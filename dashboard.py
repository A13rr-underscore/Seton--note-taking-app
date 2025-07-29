import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import tkinter as tk
import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect("Seton.db")
cursor = conn.cursor()

# Create the Seton table if it doesn't exist
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
        folder INTEGER
    )
''')
conn.commit()

def open_note_app(parent):
    """
    Open the Note App as a Toplevel window after successful login.
    This is the main dashboard of the application.
    """
    # Set theme for the dashboard
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    # Create the main dashboard window
    note_app = ctk.CTkToplevel(parent)
    note_app.title("Note App")
    note_app.geometry("1000x600")
    note_app.resizable(True, True)
    note_app.focus_force()

    # ------------- Sidebar -------------
    sidebar = ctk.CTkFrame(master=note_app, width=200)
    sidebar.pack(side="left", fill="y")
    # Placeholder for logo (replace with actual image or widget)
    ctk.CTkLabel(sidebar, text="Logo", font=("Arial", 20)).pack(pady=20)
    # Button to open the list of notes
    ctk.CTkButton(sidebar, text="Notes List", command=open_notes_list).pack(pady=10)
    # Button to open account settings (currently linked to open_blank_note, may need adjustment)
    ctk.CTkButton(sidebar, text="Account", command=open_blank_note).pack(pady=10)
    # Button to log out
    ctk.CTkButton(sidebar, text="Log Out", command=logout).pack(pady=10)

    # ------------- Header -------------
    header = ctk.CTkFrame(master=note_app, height=50)
    header.pack(fill="x")
    # Greeting label (replace "user" with actual username if available)
    ctk.CTkLabel(header, text="Hello, user!", font=("Arial", 18)).pack(side="left", padx=20)
    # Search bar for notes
    search_bar = ctk.CTkEntry(header, placeholder_text="Search notes...", width=200)
    search_bar.pack(side="right", padx=20)

    # ------------- Main Area -------------
    main_area = ctk.CTkFrame(master=note_app)
    main_area.pack(fill="both", expand=True)
    # Buttons for creating different types of notes
    cards = [
        ("Blank Note", open_blank_note),
        ("Journal", open_journal),
        ("Lecture Note", open_lecture_note),
    ]
    for idx, (label, func) in enumerate(cards):
        ctk.CTkButton(master=main_area, text=label, width=150, height=200, command=func)\
            .grid(row=0, column=idx, padx=20, pady=40)

    # ------------- Window Close Protocol -------------
    def on_close():
        # Reset theme for welcome window
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        parent.deiconify()  # Show the welcome window again
        note_app.destroy()

    note_app.protocol("WM_DELETE_WINDOW", on_close)

# ------------- Logout Function -------------
def logout():
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        def open_and_destroy():
            open_welcome_window()  # Reopen the welcome window
            note_app.destroy()     # Close the dashboard
        note_app.after(200, open_and_destroy)
