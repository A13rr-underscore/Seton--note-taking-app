import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from database import cursor

def open_login_window(parent):
    login_app = ctk.CTkToplevel(parent)
    login_app.title("Login")
    login_app.geometry("900x650")
    login_app.resizable(False, False)
    login_app.transient(parent)
    login_app.grab_set()
    login_app.focus()

    bg_pil = Image.open("hoo.jpg").resize((900, 650))
    bg_image = ctk.CTkImage(bg_pil, size=(900, 650))
    ctk.CTkLabel(login_app, image=bg_image, text="").place(relx=0, rely=0, relwidth=1, relheight=1)
    login_frame = ctk.CTkFrame(login_app, width=500, height=400, corner_radius=0, fg_color="#14222b")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")
    login_frame.pack_propagate(False)
    ctk.CTkLabel(login_frame, text="Login", font=ctk.CTkFont(size=26, weight="bold"), text_color="white").pack(pady=(40, 30))
    username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=350)
    username_entry.pack(pady=10)
    password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=350)
    password_entry.pack(pady=10)

    def do_login():
        from dashboard import open_note_app
        global current_user
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return
        cursor.execute("SELECT password FROM Users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result and result[0] == password:
            current_user = username
            messagebox.showinfo("Login", f"Welcome back, {username}!")
            login_app.destroy()
            parent.withdraw()
            open_note_app(parent)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    ctk.CTkButton(login_frame, text="Login", command=do_login, width=200).pack(pady=20)

    def go_to_recover(_event):
        from recover import open_recover_window
        login_app.destroy()
        open_recover_window(parent)

    forgot_label = ctk.CTkLabel(login_frame, text="Forgot Password?", text_color="#3a6df0", cursor="hand2")
    forgot_label.pack(pady=(5, 0))
    forgot_label.bind("<Button-1>", go_to_recover)

    def go_to_register(_event):
        from register import open_register_window
        login_app.destroy()
        open_register_window(parent)

    signup_label = ctk.CTkLabel(login_frame, text="Don't have an account? Create one",
                                text_color="#3a6df0", cursor="hand2")
    signup_label.pack(pady=(10, 0))
    signup_label.bind("<Button-1>", go_to_register)