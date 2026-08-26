import tkinter as tk
from tkinter import messagebox

MATTE_BLACK = "#101010"
CARD = "#181818"
BLOOD_RED = "#8B0000"
OCEAN_BLUE = "#006994"
MILKY_WHITE = "#F5F1E8"
MUTED = "#A8A8A8"


def dashboard(root):
    for widget in root.winfo_children():
        widget.destroy()

    sidebar = tk.Frame(root, bg="#0B0B0B", width=245)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="🚗", font=("Segoe UI Emoji", 34), fg=MILKY_WHITE, bg="#0B0B0B").pack(pady=(30, 0))
    tk.Label(sidebar, text="AutoMaster", font=("Segoe UI", 20, "bold"), fg=MILKY_WHITE, bg="#0B0B0B").pack()
    tk.Label(sidebar, text="PRO", font=("Segoe UI", 10, "bold"), fg=OCEAN_BLUE, bg="#0B0B0B").pack(pady=(0, 25))

    items = ["🏠  داشبورد", "👥  کاربران", "🚘  خودروها", "👤  مشتریان", "🔧  تعمیرات", "👨‍🔧  مکانیک‌ها", "📦  قطعات", "💰  فاکتورها", "📊  گزارش‌ها"]
    for item in items:
        tk.Button(sidebar, text=item, font=("Tahoma", 11, "bold"), anchor="w", bd=0, relief="flat", cursor="hand2",
                  bg="#0B0B0B", fg=MILKY_WHITE, activebackground=BLOOD_RED, activeforeground=MILKY_WHITE,
                  padx=22, pady=11).pack(fill="x", padx=10, pady=2)

    tk.Button(sidebar, text="⚙  تنظیمات", font=("Tahoma", 11), anchor="w", bd=0, relief="flat", cursor="hand2",
              bg="#0B0B0B", fg=MUTED, activebackground=OCEAN_BLUE, activeforeground=MILKY_WHITE,
              padx=22, pady=11).pack(side="bottom", fill="x", padx=10, pady=20)

    content = tk.Frame(root, bg=MATTE_BLACK)
    content.pack(side="left", fill="both", expand=True)

    top = tk.Frame(content, bg=MATTE_BLACK, height=85)
    top.pack(fill="x", padx=28, pady=(18, 0))
    top.pack_propagate(False)
    tk.Label(top, text="داشبورد مدیریت", font=("Tahoma", 23, "bold"), fg=MILKY_WHITE, bg=MATTE_BLACK).pack(side="left", pady=20)
    tk.Label(top, text="مدیریت حرفه‌ای خودرو و تعمیرگاه", font=("Tahoma", 10), fg=OCEAN_BLUE, bg=MATTE_BLACK).pack(side="right", pady=25)

    stats = tk.Frame(content, bg=MATTE_BLACK)
    stats.pack(fill="x", padx=28)
    cards = [("🚘", "خودروها", "0", BLOOD_RED), ("👤", "مشتریان", "0", OCEAN_BLUE), ("🔧", "تعمیرات", "0", BLOOD_RED), ("💰", "درآمد", "0 تومان", OCEAN_BLUE)]
    for icon, title, value, accent in cards:
        card = tk.Frame(stats, bg=CARD, highlightbackground=accent, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=6, pady=8, ipady=15)
        tk.Label(card, text=icon, font=("Segoe UI Emoji", 23), bg=CARD, fg=MILKY_WHITE).pack(anchor="w", padx=18)
        tk.Label(card, text=title, font=("Tahoma", 10), bg=CARD, fg=MUTED).pack(anchor="w", padx=18)
        tk.Label(card, text=value, font=("Segoe UI", 19, "bold"), bg=CARD, fg=MILKY_WHITE).pack(anchor="w", padx=18, pady=(4, 0))

    hero = tk.Frame(content, bg=CARD, highlightbackground=OCEAN_BLUE, highlightthickness=1)
    hero.pack(fill="both", expand=True, padx=34, pady=20)
    tk.Label(hero, text="خودروی منتخب", font=("Tahoma", 16, "bold"), fg=MILKY_WHITE, bg=CARD).pack(anchor="e", padx=28, pady=(24, 5))
    tk.Label(hero, text="تصویر خودرو پس از ثبت خودرو در این قسمت نمایش داده می‌شود", font=("Tahoma", 12), fg=MUTED, bg=CARD).pack(pady=75)
    tk.Label(hero, text="مدیریت خودروها  •  مشتریان  •  تعمیرات  •  قطعات  •  فاکتورها", font=("Tahoma", 10), fg=OCEAN_BLUE, bg=CARD).pack(pady=15)


def login(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=MATTE_BLACK)
    box = tk.Frame(root, bg=CARD, highlightbackground=BLOOD_RED, highlightthickness=1)
    box.place(relx=0.5, rely=0.5, anchor="center", width=440, height=450)

    tk.Label(box, text="🚗", font=("Segoe UI Emoji", 42), fg=MILKY_WHITE, bg=CARD).pack(pady=(28, 0))
    tk.Label(box, text="AutoMaster Pro", font=("Segoe UI", 25, "bold"), fg=MILKY_WHITE, bg=CARD).pack()
    tk.Label(box, text="ورود به سیستم مدیریت تعمیرگاه", font=("Tahoma", 11), fg=OCEAN_BLUE, bg=CARD).pack(pady=(0, 25))

    tk.Label(box, text="نام کاربری", font=("Tahoma", 10, "bold"), fg=MILKY_WHITE, bg=CARD).pack(anchor="e", padx=55)
    username = tk.Entry(box, font=("Tahoma", 12), bg="#252525", fg=MILKY_WHITE, insertbackground=MILKY_WHITE, relief="flat", justify="right")
    username.pack(fill="x", padx=55, ipady=10, pady=(5, 15))

    tk.Label(box, text="رمز عبور", font=("Tahoma", 10, "bold"), fg=MILKY_WHITE, bg=CARD).pack(anchor="e", padx=55)
    password = tk.Entry(box, font=("Tahoma", 12), bg="#252525", fg=MILKY_WHITE, insertbackground=MILKY_WHITE, relief="flat", justify="right", show="•")
    password.pack(fill="x", padx=55, ipady=10, pady=(5, 4))

    def toggle():
        password.config(show="" if password.cget("show") else "•")

    tk.Button(box, text="نمایش / مخفی کردن رمز", command=toggle, bg=CARD, fg=OCEAN_BLUE, bd=0, cursor="hand2", font=("Tahoma", 9)).pack(anchor="e", padx=55)

    def enter():
        if username.get() and password.get():
            dashboard(root)
        else:
            messagebox.showwarning("ورود", "نام کاربری و رمز عبور را وارد کنید.")

    tk.Button(box, text="ورود به سیستم", command=enter, font=("Tahoma", 12, "bold"), bg=BLOOD_RED, fg=MILKY_WHITE,
              activebackground=OCEAN_BLUE, activeforeground=MILKY_WHITE, bd=0, relief="flat", cursor="hand2", pady=12).pack(fill="x", padx=55, pady=22)


def start_application():
    root = tk.Tk()
    root.title("AutoMaster Pro")
    root.geometry("1280x760")
    root.minsize(1050, 650)
    root.configure(bg=MATTE_BLACK)
    login(root)
    root.mainloop()


if __name__ == "__main__":
    start_application()
