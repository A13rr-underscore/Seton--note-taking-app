import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import tkinter as tk
import sqlite3

from database import cursor, conn
from register import open_account_window
def open_account_window(parent):
    account_app = ctk.CTkToplevel(parent)
    account_app.title("User Information")
    account_app.geometry("400x300")
    account_app.transient(parent)
    account_app.grab_set()
    account_app.focus_force()

    cursor.execute("SELECT username, password FROM Users WHERE username = ?", (current_user,))
    user_data = cursor.fetchone()

    def go_back():
        account_app.destroy()

    ctk.CTkButton(account_app, text="< Back", command=go_back, width=60).pack(anchor="nw", padx=10, pady=10)
    frame = ctk.CTkFrame(account_app)
    frame.pack(expand=True, padx=20, pady=20)
    ctk.CTkLabel(frame, text="User Information", font=("Arial", 18)).pack(pady=10)
    username_frame = ctk.CTkFrame(frame)
    username_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(username_frame, text="username:", font=("Arial", 14)).pack(side="left")
    ctk.CTkLabel(username_frame, text=user_data[0], font=("Arial", 14)).pack(side="left", padx=10)
    ctk.CTkButton(username_frame, text="Update", command=lambda: open_change_username_window(account_app), width=80).pack(side="right")
    password_frame = ctk.CTkFrame(frame)
    password_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(password_frame, text="password:", font=("Arial", 14)).pack(side="left")
    ctk.CTkLabel(password_frame, text="********", font=("Arial", 14)).pack(side="left", padx=10)
    ctk.CTkButton(password_frame, text="Update", command=lambda: open_change_password_window(account_app), width=80).pack(side="right")

def open_change_username_window(parent):
    change_username_app = ctk.CTkToplevel(parent)
    change_username_app.title("Change username")
    change_username_app.geometry("400x300")
    change_username_app.transient(parent)
    change_username_app.grab_set()
    change_username_app.focus_force()

    def go_back():
        change_username_app.destroy()

    ctk.CTkButton(change_username_app, text="< Back", command=go_back, width=60).pack(anchor="nw", padx=10, pady=10)
    frame = ctk.CTkFrame(change_username_app)
    frame.pack(expand=True, padx=20, pady=20)
    ctk.CTkLabel(frame, text="Change username", font=("Arial", 18)).pack(pady=10)
    cursor.execute("SELECT username FROM Users WHERE username = ?", (current_user,))
    current_username = cursor.fetchone()[0]
    username_frame = ctk.CTkFrame(frame)
    username_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(username_frame, text="New username:", font=("Arial", 14)).pack(side="left")
    new_username_entry = ctk.CTkEntry(username_frame, width=200)
    new_username_entry.insert(0, current_username)
    new_username_entry.pack(side="left", padx=10)
    password_frame = ctk.CTkFrame(frame)
    password_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(password_frame, text="password:", font=("Arial", 14)).pack(side="left")
    password_entry = ctk.CTkEntry(password_frame, show="*", width=200)
    password_entry.pack(side="left", padx=10)

    def update_username():
        global current_user
        new_username = new_username_entry.get()
        password = password_entry.get()
        if not new_username or not password:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return
        cursor.execute("SELECT password FROM Users WHERE username = ?", (current_user,))
        stored_password = cursor.fetchone()
        if stored_password and stored_password[0] == password:
            cursor.execute("SELECT username FROM Users WHERE username = ?", (new_username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists.")
                return
            cursor.execute("UPDATE Users SET username = ? WHERE username = ?", (new_username, current_user))
            cursor.execute("UPDATE Seton SET username = ? WHERE username = ?", (new_username, current_user))
            conn.commit()
            current_user = new_username
            messagebox.showinfo("Success", "Username updated successfully!")
            change_username_app.destroy()
            parent.destroy()
            open_account_window(parent.master)
        else:
            messagebox.showerror("Error", "Incorrect password.")

    ctk.CTkButton(frame, text="Update", command=update_username, width=80).pack(pady=20)

def open_change_password_window(parent):
    change_password_app = ctk.CTkToplevel(parent)
    change_password_app.title("Change password")
    change_password_app.geometry("500x400")
    change_password_app.transient(parent)
    change_password_app.grab_set()
    change_password_app.focus_force()

    def go_back():
        change_password_app.destroy()

    ctk.CTkButton(change_password_app, text="< Back", command=go_back, width=60).pack(anchor="nw", padx=10, pady=10)
    frame = ctk.CTkFrame(change_password_app)
    frame.pack(expand=True, padx=20, pady=20)
    ctk.CTkLabel(frame, text="Change password", font=("Arial", 18)).pack(pady=10)
    old_password_frame = ctk.CTkFrame(frame)
    old_password_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(old_password_frame, text="Old password:", font=("Arial", 14)).pack(side="left")
    old_password_entry = ctk.CTkEntry(old_password_frame, show="*", width=200)
    old_password_entry.pack(side="left", padx=10)
    new_password_frame = ctk.CTkFrame(frame)
    new_password_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(new_password_frame, text="New password:", font=("Arial", 14)).pack(side="left")
    new_password_entry = ctk.CTkEntry(new_password_frame, show="*", width=200)
    new_password_entry.pack(side="left", padx=10)
    confirm_password_frame = ctk.CTkFrame(frame)
    confirm_password_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(confirm_password_frame, text="Confirm password:", font=("Arial", 14)).pack(side="left")
    confirm_password_entry = ctk.CTkEntry(confirm_password_frame, show="*", width=200)
    confirm_password_entry.pack(side="left", padx=10)

    def update_password():
        global current_user
        old_password = old_password_entry.get()
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()
        if not all([old_password, new_password, confirm_password]):
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return
        cursor.execute("SELECT password FROM Users WHERE username = ?", (current_user,))
        stored_password = cursor.fetchone()
        if stored_password and stored_password[0] == old_password:
            if new_password != confirm_password:
                messagebox.showerror("Mismatch", "New passwords do not match.")
                return
            cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (new_password, current_user))
            conn.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
            change_password_app.destroy()
            parent.destroy()
            open_account_window(parent.master)
        else:
            messagebox.showerror("Error", "Incorrect old password.")

    ctk.CTkButton(frame, text="Update", command=update_password, width=120, height=50).pack(pady=20)
