from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime
root = Tk()
root.geometry('800x500')

def login_window():
    name.grid_forget()
    name_input.grid_forget()
    email.grid_forget()
    email_input.grid_forget()
    password.grid_forget()
    reg_password_input.grid_forget()
    hidePass_btn.grid_forget()
    confirm_password.grid_forget()
    reg_confirm.grid_forget()
    hideCon_btn.grid_forget()
    register.grid_forget()
    back.grid_forget()
    username.grid(row=1, column=0)
    username_input.grid(row=1, column=1)
    password.grid(row=2, column=0)
    password_input.grid(row=2, column=1)
    hide_btn.grid(row=2, column=2)
    login.grid(row=5, column=1)
    create.grid(row=6, column=1)

def register_window():
    username.grid_forget()
    username_input.grid_forget()
    password.grid_forget()
    password_input.grid_forget()
    hide_btn.grid_forget()
    login.grid_forget()
    create.grid_forget()
    name.grid(row=3, column=0)
    name_input.grid(row=3, column=1)
    email.grid(row=4, column=0)
    email_input.grid(row=4, column=1)
    password.grid(row=5, column=0)
    reg_password_input.grid(row=5, column=1)
    hidePass_btn.grid(row=5, column=2)
    confirm_password.grid(row=6, column=0)
    reg_confirm.grid(row=6, column=1)
    hideCon_btn.grid(row=6, column=2)
    register.grid(row=10, column=1)
    back.grid(row=11, column=1)

def add():
    n = name_input.get()
    e = email_input.get()
    p = reg_password_input.get()
    c = reg_confirm.get()

    if not n or not e or not p or not c:
        messagebox.showwarning('error', 'All fields are required')
        return
    
    # conn = sqlite3.connect('customer_registration.db')
    # c = conn.cursor()
    # c.execute('INSERT INTO registration (full_name, phone, email, address) \
    #           VALUES ("{}", "{}", "{}", "{}")'.format(f, p, e, a))
    # conn.commit()
    # conn.close()

    name_input.delete(0, END)
    email_input.delete(0, END)
    reg_password_input.delete(0, END)
    reg_confirm.delete(0, END)

    if reg_confirm.get() == reg_password_input.get():
        messagebox.showinfo("success!", 'account created successfully')
    else:
        messagebox.showwarning("password doesn't match", 'please enter the same password')

def showHide():
    if hide.get() == 1:
        password_input.config(show='')
    else:
        password_input.config(show='*')
    if hidePass.get() == 1:
        reg_password_input.config(show='')
    else:
        reg_password_input.config(show='*')
    if hideCon.get() == 1:
        reg_confirm.config(show='')
    else:
        reg_confirm.config(show='*')

# Label(root, text="Login").grid(row=0, column= 1)
username = Label(root, text="username")
username_input = Entry(root)
password = Label(root, text="password")
password_input = Entry(root, show='*')
hide = IntVar()
hide_btn = Checkbutton(text='show password', variable=hide, command=showHide)
login = Button(root, text="Login")
create = Button(root, text='Create Account', command=register_window)

name = Label(text="Name")
name_input = Entry()
email = Label(text="Email")
email_input = Entry()
password = Label(root,text="Password")
reg_password_input = Entry(root,show='*')
hidePass = IntVar()
hidePass_btn = Checkbutton(text='show password', variable=hidePass, command=showHide)
confirm_password = Label(root,text='Confirm Password')
reg_confirm = Entry(root,show='*')
hideCon = IntVar()
hideCon_btn = Checkbutton(text='show password', variable=hideCon, command=showHide)
register = Button(text="Register", command=add)
back = Button(text='Back to Login', command=login_window)

login_window()

mainloop()