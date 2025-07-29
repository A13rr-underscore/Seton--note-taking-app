import customtkinter as ctk
from PIL import Image

from login import open_login_window

def open_welcome_window(prev_window=None):
    root = ctk.CTk()
    root.geometry("900x600")
    root.title("Welcome Page")
    root.resizable(False, False)

    bg_pil = Image.open("wel.png").resize((900, 600))
    bg_image = ctk.CTkImage(bg_pil, size=(900, 600))
    bg_label = ctk.CTkLabel(root, image=bg_image, text="")
    bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    root.bg_image = bg_image

    ctk.CTkButton(
        root, text="Login", width=80, height=30, corner_radius=10,
        fg_color="transparent", hover_color="#000000", border_width=0,
        text_color="white", command=lambda: open_login_window(root)
    ).place(relx=0.95, y=10, anchor="ne", x=-95)
    ctk.CTkButton(
        root, text="Sign Up", width=80, height=30, corner_radius=10,
        fg_color="transparent", hover_color="#000000", border_width=0,
        text_color="white", command=lambda: open_register_window(root)
    ).place(relx=0.99, y=10, anchor="ne", x=-10)

    def cleanup():
        conn.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", cleanup)
    root.mainloop()

if __name__ == "__main__":
    open_welcome_window()
