import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import tkinter as tk

#  Global Appearance 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Global Variable for Logged-In User
current_user = None

#  Database 
conn = sqlite3.connect("Seton.db")
cursor = conn.cursor()

# Create Seton table with username field
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Seton (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT,
        category TEXT,
        mood TEXT,
        date TEXT,
        subject TEXT,
        topic TEXT,
        summary TEXT,
        folder INTEGER,
        username TEXT,
        FOREIGN KEY (username) REFERENCES Users (username)
    )
''')
conn.commit()

#                Blank Note

def open_blank_note(parent):
    editor = ctk.CTkToplevel(parent)
    editor.title("New Blank Note")
    editor.geometry("800x500")
    editor.transient(parent)
    editor.lift()
    editor.focus_force()

    def save_note():
        title = title_entry.get()
        content = content_textbox.get("1.0", "end-1c")
        if title.strip() and content.strip():
            folder = 1
            cursor.execute(
                "INSERT INTO Seton (title, content, category, folder, username) VALUES (?, ?, ?, ?, ?)",
                (title, content, "Blank Note", folder, current_user)
            )
            conn.commit()
            editor.destroy()
        else:
            messagebox.showwarning("Missing Fields", "Please provide both a title and content.")

    def delete_note():
        if tk.messagebox.askyesno("Delete", "Are you sure you want to delete this note?"):
            editor.destroy()

    def go_back():
        if tk.messagebox.askyesno("Go Back", "Are you sure you want to go back? Unsaved changes will be lost."):
            editor.destroy()

    ctk.CTkButton(editor, text="< Back", command=go_back, width=80).pack(anchor="nw", padx=10, pady=10)
    title_frame = ctk.CTkFrame(editor)
    title_frame.pack(fill="x", padx=20)
    ctk.CTkLabel(title_frame, text="Title:", font=("Arial", 16)).pack(side="left")
    title_entry = ctk.CTkEntry(title_frame, width=400, placeholder_text="Enter title...")
    title_entry.pack(side="left", padx=10)
    ctk.CTkButton(title_frame, text="Save", command=save_note, width=80).pack(side="right", padx=5)
    ctk.CTkButton(title_frame, text="Delete", command=delete_note, width=80).pack(side="right", padx=5)
    content_textbox = ctk.CTkTextbox(editor, width=760, height=380)
    content_textbox.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = ctk.CTk()
    open_blank_note(root)
    root.mainloop()
