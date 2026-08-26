import tkinter as tk
from tkinter import messagebox


# ==============================
# AutoMaster Pro
# Main File
# ==============================

def start_application():
    root = tk.Tk()

    root.title("AutoMaster Pro")
    root.geometry("1200x700")
    root.minsize(1000, 600)

    # رنگ‌های اصلی پروژه
    MATTE_BLACK = "#111111"
    BLOOD_RED = "#8B0000"
    OCEAN_BLUE = "#006994"
    MILKY_WHITE = "#F5F1E8"

    root.configure(bg=MATTE_BLACK)

    # ==============================
    # Header
    # ==============================

    header = tk.Frame(
        root,
        bg=MATTE_BLACK,
        height=90
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    title = tk.Label(
        header,
        text="AutoMaster Pro",
        font=("Segoe UI", 28, "bold"),
        fg=MILKY_WHITE,
        bg=MATTE_BLACK
    )
    title.pack(side="left", padx=35, pady=20)

    subtitle = tk.Label(
        header,
        text="سیستم حرفه‌ای مدیریت خودرو و تعمیرگاه",
        font=("Tahoma", 12),
        fg=OCEAN_BLUE,
        bg=MATTE_BLACK
    )
    subtitle.pack(side="left", padx=10)

    # ==============================
    # Main Content
    # ==============================

    main_frame = tk.Frame(
        root,
        bg=MATTE_BLACK
    )
    main_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    # کارت خوش‌آمدگویی
    welcome_card = tk.Frame(
        main_frame,
        bg="#181818",
        highlightbackground=BLOOD_RED,
        highlightthickness=1
    )
    welcome_card.pack(
        fill="both",
        expand=True
    )

    welcome_title = tk.Label(
        welcome_card,
        text="🚗 AutoMaster Pro",
        font=("Segoe UI", 32, "bold"),
        fg=MILKY_WHITE,
        bg="#181818"
    )
    welcome_title.pack(pady=(100, 15))

    welcome_text = tk.Label(
        welcome_card,
        text="سیستم مدیریت خودرو، تعمیرگاه و خدمات",
        font=("Tahoma", 16),
        fg="#CCCCCC",
        bg="#181818"
    )
    welcome_text.pack(pady=10)

    start_button = tk.Button(
        welcome_card,
        text="ورود به سیستم",
        font=("Tahoma", 14, "bold"),
        fg=MILKY_WHITE,
        bg=BLOOD_RED,
        activebackground=OCEAN_BLUE,
        activeforeground=MILKY_WHITE,
        relief="flat",
        cursor="hand2",
        padx=35,
        pady=12,
        command=lambda: messagebox.showinfo(
            "AutoMaster Pro",
            "پنل ورود در مرحله بعد ساخته می‌شود."
        )
    )
    start_button.pack(pady=35)

    # ==============================
    # Footer
    # ==============================

    footer = tk.Label(
        root,
        text="AutoMaster Pro © 2026",
        font=("Segoe UI", 9),
        fg="#777777",
        bg=MATTE_BLACK
    )
    footer.pack(side="bottom", pady=10)

    root.mainloop()


# اجرای برنامه
if __name__ == "__main__":
    start_application()
