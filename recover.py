import customtkinter as ctk
from tkinter import messagebox

from database import cursor

def open_recover_window(parent):
    recover_app = ctk.CTkToplevel(parent)
    recover_app.title("Recover Account")
    recover_app.geometry("900x650")
    recover_app.resizable(False, False)
    recover_app.transient(parent)
    recover_app.grab_set()
    recover_app.focus()

    bg_pil = Image.open("hoo.jpg").resize((900, 650))
    bg_image = ctk.CTkImage(bg_pil, size=(900, 650))
    bg_label = ctk.CTkLabel(recover_app, image=bg_image, text="")
    bg_label.image = bg_image
    bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    recover_frame = ctk.CTkFrame(recover_app, width=500, height=550, corner_radius=10, fg_color="#14222b")
    recover_frame.place(relx=0.5, rely=0.5, anchor="center")
    recover_frame.pack_propagate(False)
    ctk.CTkLabel(recover_frame, text="Recover Your Account", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(40, 30))
    ctk.CTkLabel(recover_frame, text="Username:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
    username_entry = ctk.CTkEntry(recover_frame, placeholder_text="Username", width=300, font=ctk.CTkFont(size=14), text_color="white")
    username_entry.pack(pady=(0, 20))
    ctk.CTkLabel(recover_frame, text="What was your childhood nickname?", font=ctk.CTkFont(size=12)).pack(pady=5)
    ans1_entry = ctk.CTkEntry(recover_frame, placeholder_text="Answer", width=300, font=ctk.CTkFont(size=14), text_color="white")
    ans1_entry.pack(pady=6)
    ctk.CTkLabel(recover_frame, text="What was the name of your first pet?", font=ctk.CTkFont(size=12)).pack(pady=5)
    ans2_entry = ctk.CTkEntry(recover_frame, placeholder_text="Answer", width=300, font=ctk.CTkFont(size=14), text_color="white")
    ans2_entry.pack(pady=6)
    entry_style = {"width": 300, "font": ctk.CTkFont(size=14), "text_color": "white", "placeholder_text_color": "#aaaaaa", "show": "*"}
    new_pass = ctk.CTkEntry(recover_frame, placeholder_text="New Password", **entry_style)
    new_pass.pack(pady=(30, 30))
    confirm_pass = ctk.CTkEntry(recover_frame, placeholder_text="Confirm Password", **entry_style)
    confirm_pass.pack(pady=(5, 30))

    def recover():
        username = username_entry.get()
        ans1 = ans1_entry.get()
        ans2 = ans2_entry.get()
        new_password = new_pass.get()
        confirm_password = confirm_pass.get()
        if not all([username, ans1, ans2, new_password, confirm_password]):
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
        elif new_password != confirm_password:
            messagebox.showerror("Mismatch", "Passwords do not match.")
        else:
            cursor.execute("SELECT answer1, answer2 FROM Users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result and result[0] == ans1 and result[1] == ans2:
                cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (new_password, username))
                conn.commit()
                messagebox.showinfo("Success", "Password successfully updated!")
                recover_app.destroy()
                open_login_window(parent)
            else:
                messagebox.showerror("Error", "Incorrect answers or username.")

    ctk.CTkButton(recover_frame, text="Recover", command=recover, width=200, height=40,
                  font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)