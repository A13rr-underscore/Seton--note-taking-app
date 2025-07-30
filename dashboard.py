import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import tkinter as tk
from datetime import datetime

from database import cursor, conn
from account import open_account_window
from login import open_login_window

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ---------------- Global Variable for Logged-In User ----------------
current_user = None

def open_note_app(parent):
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    note_app = ctk.CTkToplevel(parent)
    note_app.title("Note App")
    note_app.geometry("1000x600")
    note_app.resizable(True, True)
    note_app.focus_force()

    
    def open_notes_list():
        window = ctk.CTkToplevel(note_app)
        window.title("Notes List")
        window.geometry("900x600")
        window.transient(note_app)
        window.lift()
        window.focus_force()

        current_folder = None
        notes = []

        def go_back():
            window.destroy()

        def delete_note():
            selected = notes_listbox.curselection()
            if selected:
                note_id = notes[selected[0]][0]
                if tk.messagebox.askyesno("Delete", "Are you sure you want to delete this note?"):
                    cursor.execute("DELETE FROM Seton WHERE id=? AND username=?", (note_id, current_user))
                    conn.commit()
                    refresh_notes()

        def open_note():
            selected = notes_listbox.curselection()
            if selected:
                note_id = notes[selected[0]][0]
                title = notes[selected[0]][1]
                content = notes[selected[0]][2]
                date = notes[selected[0]][3]
                mood = notes[selected[0]][4]
                subject = notes[selected[0]][5]
                topic = notes[selected[0]][6]
                summary = notes[selected[0]][7]
                folder = current_folder

                editor = ctk.CTkToplevel(window)
                editor.title(title)
                editor.geometry("800x600")
                editor.transient(note_app)
                editor.grab_set()
                editor.focus_force()

                def save_changes():
                    updated_title = title_entry.get()
                    updated_content = content_textbox.get("1.0", "end-1c")
                    if updated_title.strip() and updated_content.strip():
                        if folder == 2:  # Journals
                            updated_date = date_entry.get()
                            updated_mood = mood_entry.get()
                            cursor.execute(
                                "UPDATE Seton SET title=?, content=?, date=?, mood=? WHERE id=? AND username=?",
                                (updated_title, updated_content, updated_date, updated_mood, note_id, current_user)
                            )
                        elif folder == 3:  # Lecture Notes
                            updated_date = date_entry.get()
                            updated_subject = subject_entry.get()
                            updated_topic = topic_entry.get()
                            updated_summary = summary_textbox.get("1.0", "end-1c")
                            cursor.execute(
                                "UPDATE Seton SET title=?, content=?, date=?, subject=?, topic=?, summary=? WHERE id=? AND username=?",
                                (updated_title, updated_content, updated_date, updated_subject, updated_topic, updated_summary, note_id, current_user)
                            )
                        else:  # Blank Notes
                            cursor.execute(
                                "UPDATE Seton SET title=?, content=? WHERE id=? AND username=?",
                                (updated_title, updated_content, note_id, current_user)
                            )
                        conn.commit()
                        editor.destroy()
                        refresh_notes()

                ctk.CTkButton(editor, text="< Back", command=editor.destroy, width=80).pack(anchor="nw", padx=10, pady=10)
                title_frame = ctk.CTkFrame(editor)
                title_frame.pack(fill="x", padx=20)
                ctk.CTkLabel(title_frame, text="Title:", font=("Arial", 16)).pack(side="left")
                title_entry = ctk.CTkEntry(title_frame, width=400)
                title_entry.insert(0, title)
                title_entry.pack(side="left", padx=10)
                ctk.CTkButton(title_frame, text="Save", command=save_changes, width=80).pack(side="right", padx=5)
                if folder == 2:  # Journals
                    form_frame = ctk.CTkFrame(editor)
                    form_frame.pack(fill="x", padx=20, pady=10)
                    ctk.CTkLabel(form_frame, text="Date:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=5)
                    date_entry = ctk.CTkEntry(form_frame, width=150)
                    date_entry.insert(0, date if date else datetime.today().strftime('%d/%m/%Y'))
                    date_entry.grid(row=0, column=1, padx=10, pady=5)
                    ctk.CTkLabel(form_frame, text="Mood:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=5)
                    mood_entry = ctk.CTkEntry(form_frame, width=300)
                    mood_entry.insert(0, mood if mood else "")
                    mood_entry.grid(row=1, column=1, padx=10, pady=5)
                    content_textbox = ctk.CTkTextbox(editor, width=760, height=300)
                elif folder == 3:  # Lecture Notes
                    info_frame = ctk.CTkFrame(editor)
                    info_frame.pack(fill="x", padx=20, pady=10)
                    ctk.CTkLabel(info_frame, text="Subject:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=5)
                    subject_entry = ctk.CTkEntry(info_frame, width=250)
                    subject_entry.insert(0, subject if subject else "")
                    subject_entry.grid(row=0, column=1, padx=10, pady=5)
                    ctk.CTkLabel(info_frame, text="Topic:", font=("Arial", 14)).grid(row=0, column=2, sticky="w", pady=5)
                    topic_entry = ctk.CTkEntry(info_frame, width=250)
                    topic_entry.insert(0, topic if topic else "")
                    topic_entry.grid(row=0, column=3, padx=10, pady=5)
                    ctk.CTkLabel(info_frame, text="Date:", font=("Arial", 14)).grid(row=0, column=4, sticky="w", pady=5)
                    date_entry = ctk.CTkEntry(info_frame, width=120)
                    date_entry.insert(0, date if date else datetime.today().strftime('%d/%m/%Y'))
                    date_entry.grid(row=0, column=5, padx=10, pady=5)
                    content_textbox = ctk.CTkTextbox(editor, width=760, height=250)
                    content_textbox.pack(padx=20, pady=10)
                    summary_textbox = ctk.CTkTextbox(editor, width=760, height=100)
                    summary_textbox.insert("1.0", summary if summary else "Write summary / key points here...")
                    summary_textbox.pack(padx=20, pady=10)
                else:  # Blank Notes
                    content_textbox = ctk.CTkTextbox(editor, width=760, height=380)
                content_textbox.insert("1.0", content)
                content_textbox.pack(padx=20, pady=20)

        top_frame = ctk.CTkFrame(window)
        top_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(top_frame, text="< Back", command=go_back, width=60).pack(side="left")
        ctk.CTkLabel(top_frame, text="List of Notes", font=("Arial", 18)).pack(side="left", padx=20)
        bottom_frame = ctk.CTkFrame(window)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)
        folders_frame = ctk.CTkFrame(bottom_frame, width=200)
        folders_frame.pack(side="left", fill="y")

        def filter_folder(folder_num):
            nonlocal current_folder
            current_folder = folder_num
            refresh_notes()

        ctk.CTkButton(folders_frame, text="Notes", command=lambda: filter_folder(1)).pack(pady=5, fill="x", padx=5)
        ctk.CTkButton(folders_frame, text="Journals", command=lambda: filter_folder(2)).pack(pady=5, fill="x", padx=5)
        ctk.CTkButton(folders_frame, text="Lecture Notes", command=lambda: filter_folder(3)).pack(pady=5, fill="x", padx=5)
        notes_frame = ctk.CTkFrame(bottom_frame)
        notes_frame.pack(side="left", fill="both", expand=True, padx=10)
        notes_listbox = tk.Listbox(notes_frame, height=20, font=("Arial", 18), fg="black")
        notes_listbox.pack(fill="both", expand=True)
        button_frame = ctk.CTkFrame(window)
        button_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Open", command=open_note).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Delete", command=delete_note).pack(side="right")

        def refresh_notes():
            nonlocal notes
            if current_folder:
                cursor.execute("SELECT id, title, content, date, mood, subject, topic, summary FROM Seton WHERE folder=? AND username=?", (current_folder, current_user))
            else:
                cursor.execute("SELECT id, title, content, date, mood, subject, topic, summary FROM Seton WHERE username=?", (current_user,))
            notes = cursor.fetchall()
            notes_listbox.delete(0, "end")
            for note in notes:
                title = note[1]
                if current_folder == 2:  # Journals
                    date = note[3] if note[3] else "No Date"
                    mood = note[4] if note[4] else "No Mood"
                    display_text = f"{title} - {date} - {mood}"
                else:
                    display_text = title
                notes_listbox.insert("end", display_text)

        current_folder = 1
        refresh_notes()
    def open_blank_note():
        editor = ctk.CTkToplevel(note_app)
        editor.title("New Blank Note")
        editor.geometry("800x500")
        editor.transient(note_app)
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
    def open_journal():
        journal = ctk.CTkToplevel(note_app)
        journal.title("Journal Entry")
        journal.geometry("850x550")
        journal.transient(note_app)
        journal.lift()
        journal.focus_force()

        def save_journal():
            mood = mood_entry.get()
            title = title_entry.get()
            content = journal_text.get("1.0", "end-1c")
            date = date_entry.get()
            if title.strip() and content.strip():
                folder = 2
                cursor.execute(
                    "INSERT INTO Seton (title, content, category, mood, date, folder, username) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (title, content, "Journal", mood, date, folder, current_user)
                )
                conn.commit()
                journal.destroy()

        def delete_journal():
            if tk.messagebox.askyesno("Delete", "Are you sure you want to delete this journal entry?"):
                journal.destroy()

       def go_back():
            if tk.messagebox.askyesno("Go Back", "Are you sure you want to go back? Unsaved changes will be lost."):
                journal.destroy()

        top_frame = ctk.CTkFrame(journal)
        top_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkButton(top_frame, text="< Back", width=60, command=go_back).pack(side="left")
        ctk.CTkLabel(top_frame, text="Journal Entry -", font=("Arial", 16)).pack(side="left", padx=10)
        date_entry = ctk.CTkEntry(top_frame, width=150)
        date_entry.insert(0, datetime.today().strftime('%d/%m/%Y'))
        date_entry.pack(side="left")
        ctk.CTkButton(top_frame, text="Save", command=save_journal, width=80).pack(side="right", padx=10)
        ctk.CTkButton(top_frame, text="Delete", command=delete_journal, width=80).pack(side="right")
        form_frame = ctk.CTkFrame(journal)
        form_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(form_frame, text="Mood:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=5)
        mood_entry = ctk.CTkEntry(form_frame, width=300)
        mood_entry.grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(form_frame, text="Title:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=5)
        title_entry = ctk.CTkEntry(form_frame, width=300)
        title_entry.grid(row=1, column=1, padx=10, pady=5)
        journal_text = ctk.CTkTextbox(journal, width=780, height=350)
        journal_text.insert("1.0", "Write your journal here...")
        journal_text.pack(padx=20, pady=20)
    def open_lecture_note():
        lecture = ctk.CTkToplevel(note_app)
        lecture.title("Lecture Note")
        lecture.geometry("850x600")
        lecture.transient(note_app)
        lecture.lift()
        lecture.focus_force()

        def save_lecture():
            title = title_entry.get()
            subject = subject_entry.get()
            topic = topic_entry.get()
            date = date_entry.get()
            content = notes_text.get("1.0", "end-1c")
            summary = summary_text.get("1.0", "end-1c")
            if title.strip() and content.strip():
                folder = 3
                cursor.execute(
                    "INSERT INTO Seton (title, content, category, date, subject, topic, summary, folder, username) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (title, content, "Lecture", date, subject, topic, summary, folder, current_user)
                )
                conn.commit()
                lecture.destroy()

        def delete_lecture():
            if tk.messagebox.askyesno("Delete", "Are you sure you want to delete this lecture note?"):
                lecture.destroy()

        def go_back():
            if tk.messagebox.askyesno("Go Back", "Are you sure you want to go back? Unsaved changes will be lost."):
                lecture.destroy()

        top_frame = ctk.CTkFrame(lecture)
        top_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkButton(top_frame, text="< Back", width=60, command=go_back).pack(side="left")
        ctk.CTkLabel(top_frame, text="Title:", font=("Arial", 16)).pack(side="left", padx=10)
        title_entry = ctk.CTkEntry(top_frame, width=300)
        title_entry.pack(side="left", padx=10)
        ctk.CTkButton(top_frame, text="Save", width=80, command=save_lecture).pack(side="right", padx=5)
        ctk.CTkButton(top_frame, text="Delete", width=80, command=delete_lecture).pack(side="right", padx=5)
        info_frame = ctk.CTkFrame(lecture)
        info_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(info_frame, text="Subject:", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=5)
        subject_entry = ctk.CTkEntry(info_frame, width=250)
        subject_entry.grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(info_frame, text="Topic:", font=("Arial", 14)).grid(row=0, column=2, sticky="w", pady=5)
        topic_entry = ctk.CTkEntry(info_frame, width=250)
        topic_entry.grid(row=0, column=3, padx=10, pady=5)
        ctk.CTkLabel(info_frame, text="Date:", font=("Arial", 14)).grid(row=0, column=4, sticky="w", pady=5)
        date_entry = ctk.CTkEntry(info_frame, width=120)
        date_entry.insert(0, datetime.today().strftime('%d/%m/%Y'))
        date_entry.grid(row=0, column=5, padx=10, pady=5)
        notes_text = ctk.CTkTextbox(lecture, width=780, height=250)
        notes_text.insert("1.0", "Write your lecture notes here...")
        notes_text.pack(padx=20, pady=10)
        summary_text = ctk.CTkTextbox(lecture, width=780, height=100)
        summary_text.insert("1.0", "Write summary / key points here...")
        summary_text.pack(padx=20, pady=10)

    sidebar = ctk.CTkFrame(master=note_app, width=200)
    sidebar.pack(side="left", fill="y")
    logo_image = ctk.CTkImage(
        light_image=Image.open("logo1.jpg"),
        dark_image=Image.open("logo1.jpg"),
        size=(120, 120)
    )
    ctk.CTkLabel(sidebar, image=logo_image, text="").pack(pady=20)
    ctk.CTkButton(sidebar, text="Notes List", command=open_notes_list).pack(pady=10)
    ctk.CTkButton(sidebar, text="Account", command=lambda: open_account_window(note_app)).pack(pady=10)
    def logout():
        global current_user
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            current_user = None
            open_login_window(parent)
            note_app.destroy()

    ctk.CTkButton(sidebar, text="Log Out", command=logout).pack(pady=10)
