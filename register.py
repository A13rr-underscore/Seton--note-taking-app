import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from database import cursor, conn
from login import open_login_window

def open_register_window(parent):
    register_app = ctk.CTkToplevel(parent)
    register_app.title("Create Account")
    register_app.geometry("900x650")
    register_app.resizable(False, False)
    register_app.transient(parent)
    register_app.grab_set()
    register_app.focus()

    bg_pil = Image.open("hoo.jpg").resize((900, 650))
    bg_image = ctk.CTkImage(bg_pil, size=(900, 650))
    ctk.CTkLabel(register_app, image=bg_image, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    form_frame = ctk.CTkFrame(register_app, width=600, height=550, corner_radius=0, fg_color="#14222b")
    form_frame.pack(side="left", expand=True, pady=20)
    form_frame.pack_propagate(False)
    ctk.CTkLabel(form_frame, text="Register", font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(pady=(30, 10))
    entry_style = {"width": 350, "font": ctk.CTkFont(size=14), "text_color": "white", "placeholder_text_color": "#aaaaaa"}
    username_entry = ctk.CTkEntry(form_frame, placeholder_text="Username", **entry_style)
    username_entry.pack(pady=10)
    password_entry = ctk.CTkEntry(form_frame, placeholder_text="Password", show="*", **entry_style)
    password_entry.pack(pady=10)
    confirm_entry = ctk.CTkEntry(form_frame, placeholder_text="Confirm Password", show="*", **entry_style)
    confirm_entry.pack(pady=10)

    def toggle_password():
        show = "" if show_password_var.get() else "*"
        password_entry.configure(show=show)
        confirm_entry.configure(show=show)

    show_password_var = ctk.BooleanVar()
    ctk.CTkCheckBox(form_frame, text="Show Password", variable=show_password_var, command=toggle_password,
                    font=ctk.CTkFont(size=12), text_color="white").pack(pady=(0, 10))
    ctk.CTkLabel(form_frame, text="Security questions for recovery:", text_color="white",
                 font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 10))
    ctk.CTkLabel(form_frame, text="1. What was your childhood nickname?", text_color="white",
                 font=ctk.CTkFont(size=12)).pack(pady=5)
    q1_entry = ctk.CTkEntry(form_frame, placeholder_text="Answer", **entry_style)
    q1_entry.pack(pady=6)
    ctk.CTkLabel(form_frame, text="2. What was the name of your first pet?", text_color="white",
                 font=ctk.CTkFont(size=12)).pack(pady=5)
    q2_entry = ctk.CTkEntry(form_frame, placeholder_text="Answer", **entry_style)
    q2_entry.pack(pady=6)

    def register():
        username = username_entry.get()
        password = password_entry.get()
        confirm = confirm_entry.get()
        ans1 = q1_entry.get()
        ans2 = q2_entry.get()
        if not all([username, password, confirm, ans1, ans2]):
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
        elif password != confirm:
            messagebox.showerror("Password Mismatch", "Passwords do not match.")
        else:
            cursor.execute("SELECT username FROM Users WHERE username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists.")
                return
            cursor.execute(
                "INSERT INTO Users (username, password, question1, answer1, question2, answer2) VALUES (?, ?, ?, ?, ?, ?)",
                (username, password, "What was your childhood nickname?", ans1, "What was the name of your first pet?", ans2)
            )
            conn.commit()
            messagebox.showinfo("Success", f"Account created for {username}!")
            username_entry.delete(0, "end")
            password_entry.delete(0, "end")
            confirm_entry.delete(0, "end")
            q1_entry.delete(0, "end")
            q2_entry.delete(0, "end")
            register_app.destroy()
            open_login_window(parent)

    ctk.CTkButton(form_frame, text="Register", command=register, width=200, height=30,
                  fg_color="#3a6df0", hover_color="#2e57c0", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(5, 10))
    login_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    login_frame.pack(pady=(10, 10))
    ctk.CTkLabel(login_frame, text="Already have an account? ", font=ctk.CTkFont(size=12), text_color="#aaaaaa").pack(side="left")

    def on_login_click(_event):
        register_app.destroy()
        open_login_window(parent)

    login_link = ctk.CTkLabel(login_frame, text="Login", font=ctk.CTkFont(size=12, underline=True),
                              text_color="#3a6df0", cursor="hand2")
    login_link.pack(side="left")
    login_link.bind("<Button-1>", on_login_click)