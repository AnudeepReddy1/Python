# Chat application
import requests
from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from threading import Thread
import time

url = 'http://165.22.14.77:8080/Anudeep/chat2/'
def change_send_button_status(event):
	global send_button
	send_button.config(state = ('disabled' if send_msg.get() == '' else 'normal'))

def change_buttons_status(event):
	login_button.config(state = ('disabled' if user_name.get() == '' or password.get() == '' else 'normal'))
	signup_button.config(state = ('disabled' if user_name.get() == '' or password.get() == '' else 'normal'))

def send_message(event = None):
	requests.get(f'{url}InsertMessage.jsp?UserName={user_name}&Message={send_msg.get()}')
	send_msg.delete(0, last = END)

def register(user_name, password, login_window):
	response = requests.get("http://165.22.14.77:8080/Anudeep/chat2/Register.jsp?UserName="+user_name+"&Password="+password)
	if(response.text.find("success")) > 0:
		messagebox.showinfo('Success', 'Account created successfully.')
	else:
		messagebox.showinfo('Failed', 'Try with another username.')

def get_active_users():
	try:
		while True:
			response = requests.get(f'{url}ActiveUsers.jsp?UserName={user_name}')
			active_users.config(state = 'normal')
			active_users.delete(1.0, END)
			active_users.insert(END, response.text.strip().replace("<br>", ""))
			active_users.config(state = DISABLED)
			time.sleep(2)
	except:
		print("", end = '')

def get_new_messages():
	try:
		while True:
			response = requests.get(f'{url}PrintMessages.jsp?UserName={user_name}')
			chat_box.config(state = 'normal')
			if response.text.strip() != "":
				chat_box.insert(END, f'{response.text.strip()}\n')
			chat_box.config(state = DISABLED)
			time.sleep(1)
	except:
		print("", end = '')

def clear_chat():
	chat_box.config(state = 'normal')
	chat_box.delete(1.0, END)
	chat_box.config(state= DISABLED)

def chat_window(name):
	global send_msg
	global chat_box
	global chat_window
	global send_button
	global user_name
	global active_users 
	user_name = name

	chat_window = Tk()
	chat_window.geometry('500x500')
	chat_window.title('Chat window')
	chat_window.resizable(0, 0)
	chat_window.bind("<FocusIn>", change_send_button_status)
	chat_window.bind("<ButtonRelease>", change_send_button_status)
	active_users_lbl = Label(chat_window, text = 'Active users')
	active_users_lbl.place(x = 300, y = 10)

	active_users = Text(chat_window, height = 5, width = 25)
	active_users.place(x = 300, y = 30)
	active_users.config(state = DISABLED)

	send_msg_lbl = Label(chat_window, text = 'Enter message: ')
	send_msg_lbl.place(x = 10, y = 400)

	send_msg = Entry(chat_window, width = 20)
	send_msg.bind("<Return>", send_message)
	send_msg.place(x = 140, y = 400)
	send_msg.focus_set()

	send_button = Button(chat_window, text = 'Send', command = send_message)
	send_button.place(x = 140, y = 430)

	clear_button = Button(chat_window, text = 'Clear', command = clear_chat)
	clear_button.place(x = 200, y = 430)

	chat_box = scrolledtext.ScrolledText(width = 30, height = 20)
	# chat_box = Text(window,  height = 20, width = 25)
	chat_box.place(x = 10, y = 10)
	chat_box.config(state = DISABLED)
	Thread(target = get_active_users).start()
	Thread(target = get_new_messages).start()

	chat_window.bind("<Key>", change_send_button_status)
	mainloop()


def login(user_name, password, login_window):
	response = requests.get(f'{url}Login.jsp?UserName={user_name}&Password={password}')
	if(response.text.find("success")) > 0:
		messagebox.showinfo('Login', 'Welcome.')
		login_window.destroy()
		chat_window(user_name)
	else:
		messagebox.showinfo('Login failed', 'Invalid credentials.')


def login_window():
	global user_name, password, login_button, signup_button
	login_window = Tk()
	login_window.geometry('500x500')
	login_window.title('MyChat login')
	login_window.resizable(0, 0)
	login_window.bind('<FocusIn>', change_buttons_status)

	user_name_lbl = Label(login_window, text = 'Enter username: ')
	user_name_lbl.place(x = 10, y = 10)

	user_name = Entry(login_window, width = 20)
	user_name.place(x = 160, y = 10)
	user_name.focus_set()

	password_lbl = Label(login_window, text = 'Enter password: ')
	password_lbl.place(x = 10, y = 50)

	password = Entry(login_window, width = 20)
	password.place(x = 160, y = 50)

	login_button = Button(login_window, text = 'Login', command = lambda: login(user_name.get(), password.get(), login_window))
	login_button.place(x = 160, y = 90)

	signup_button = Button(login_window, text = 'SignUp', command = lambda: register(user_name.get(), password.get(), login_window))
	signup_button.place(x = 240, y = 90)

	login_window.bind("<Key>", change_buttons_status)
	mainloop()

login_window()