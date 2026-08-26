import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import get_connection, initialize_database, dashboard_counts

MATTE_BLACK = "#101010"
DARK = "#0B0B0B"
CARD = "#181818"
FIELD = "#252525"
BLOOD_RED = "#8B0000"
OCEAN_BLUE = "#006994"
MILKY_WHITE = "#F5F1E8"
MUTED = "#A8A8A8"


class AutoMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoMaster Pro")
        self.root.geometry("1280x760")
        self.root.minsize(1080, 680)
        self.root.configure(bg=MATTE_BLACK)
        initialize_database()
        self.current_user = None
        self.content = None
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("Treeview", background=CARD, foreground=MILKY_WHITE,
                             fieldbackground=CARD, rowheight=34, font=("Tahoma", 10))
        self.style.configure("Treeview.Heading", background=DARK, foreground=MILKY_WHITE,
                             font=("Tahoma", 10, "bold"))
        self.show_login()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        frame = tk.Frame(self.root, bg=MATTE_BLACK)
        frame.pack(fill="both", expand=True)
        box = tk.Frame(frame, bg=CARD, highlightbackground=BLOOD_RED, highlightthickness=1)
        box.place(relx=.5, rely=.5, anchor="center", width=450, height=475)
        tk.Label(box, text="🚗", font=("Segoe UI Emoji", 44), bg=CARD, fg=MILKY_WHITE).pack(pady=(25, 0))
        tk.Label(box, text="AutoMaster Pro", font=("Segoe UI", 25, "bold"), bg=CARD, fg=MILKY_WHITE).pack()
        tk.Label(box, text="سیستم حرفه‌ای مدیریت خودرو و تعمیرگاه", font=("Tahoma", 10), bg=CARD, fg=OCEAN_BLUE).pack(pady=(0, 28))

        tk.Label(box, text="نام کاربری", bg=CARD, fg=MILKY_WHITE, font=("Tahoma", 10, "bold")).pack(anchor="e", padx=55)
        username = tk.Entry(box, bg=FIELD, fg=MILKY_WHITE, insertbackground=MILKY_WHITE, relief="flat", justify="right", font=("Tahoma", 12))
        username.pack(fill="x", padx=55, ipady=10, pady=(5, 16))
        tk.Label(box, text="رمز عبور", bg=CARD, fg=MILKY_WHITE, font=("Tahoma", 10, "bold")).pack(anchor="e", padx=55)
        password = tk.Entry(box, bg=FIELD, fg=MILKY_WHITE, insertbackground=MILKY_WHITE, relief="flat", justify="right", show="•", font=("Tahoma", 12))
        password.pack(fill="x", padx=55, ipady=10, pady=(5, 3))

        def toggle():
            password.configure(show="" if password.cget("show") else "•")
        tk.Button(box, text="نمایش / مخفی کردن رمز", command=toggle, bg=CARD, fg=OCEAN_BLUE, bd=0, font=("Tahoma", 9), cursor="hand2").pack(anchor="e", padx=55)

        def login():
            with get_connection() as conn:
                row = conn.execute("SELECT id, username, role FROM users WHERE username=? AND password=?", (username.get().strip(), password.get())).fetchone()
            if row:
                self.current_user = dict(row)
                self.show_dashboard()
            else:
                messagebox.showerror("ورود ناموفق", "نام کاربری یا رمز عبور اشتباه است.")

        tk.Button(box, text="ورود به سیستم", command=login, bg=BLOOD_RED, fg=MILKY_WHITE,
                  activebackground=OCEAN_BLUE, activeforeground=MILKY_WHITE, bd=0, cursor="hand2",
                  font=("Tahoma", 12, "bold"), pady=12).pack(fill="x", padx=55, pady=24)
        tk.Label(box, text="مدیر پیش‌فرض: admin  |  رمز: admin123", bg=CARD, fg=MUTED, font=("Tahoma", 8)).pack()
        username.focus_set()
        password.bind("<Return>", lambda e: login())

    def show_dashboard(self):
        self.clear()
        sidebar = tk.Frame(self.root, bg=DARK, width=245)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="🚗", font=("Segoe UI Emoji", 34), bg=DARK, fg=MILKY_WHITE).pack(pady=(25, 0))
        tk.Label(sidebar, text="AutoMaster", font=("Segoe UI", 20, "bold"), bg=DARK, fg=MILKY_WHITE).pack()
        tk.Label(sidebar, text="PRO", font=("Segoe UI", 10, "bold"), bg=DARK, fg=OCEAN_BLUE).pack(pady=(0, 22))
        menu = [
            ("🏠", "داشبورد", self.show_dashboard_page),
            ("🚘", "مدیریت خودروها", self.show_cars),
            ("👤", "مدیریت مشتریان", self.show_customers),
            ("🔧", "مدیریت تعمیرات", self.show_services),
            ("👨‍🔧", "مدیریت مکانیک‌ها", self.show_mechanics),
            ("📦", "مدیریت قطعات", self.show_parts),
            ("💰", "مدیریت فاکتورها", self.show_invoices),
            ("👥", "مدیریت کاربران", self.show_users),
            ("📊", "گزارش‌ها", self.show_reports),
        ]
        for icon, text, command in menu:
            if text == "مدیریت کاربران" and self.current_user.get("role") != "admin":
                continue
            tk.Button(sidebar, text=f"{icon}  {text}", command=command, anchor="w", bg=DARK, fg=MILKY_WHITE,
                      activebackground=BLOOD_RED, activeforeground=MILKY_WHITE, bd=0, relief="flat",
                      cursor="hand2", font=("Tahoma", 10, "bold"), padx=20, pady=10).pack(fill="x", padx=9, pady=2)
        tk.Button(sidebar, text="⚙  تنظیمات", command=self.show_settings, anchor="w", bg=DARK, fg=MUTED,
                  activebackground=OCEAN_BLUE, activeforeground=MILKY_WHITE, bd=0, cursor="hand2",
                  font=("Tahoma", 10), padx=20, pady=10).pack(side="bottom", fill="x", padx=9, pady=2)
        tk.Button(sidebar, text="↪  خروج", command=self.show_login, anchor="w", bg=DARK, fg=MILKY_WHITE,
                  activebackground=BLOOD_RED, activeforeground=MILKY_WHITE, bd=0, cursor="hand2",
                  font=("Tahoma", 10), padx=20, pady=10).pack(side="bottom", fill="x", padx=9, pady=(2, 18))
        self.content = tk.Frame(self.root, bg=MATTE_BLACK)
        self.content.pack(side="left", fill="both", expand=True)
        self.show_dashboard_page()

    def page_header(self, title, subtitle=""):
        for w in self.content.winfo_children():
            w.destroy()
        top = tk.Frame(self.content, bg=MATTE_BLACK, height=80)
        top.pack(fill="x", padx=28, pady=(16, 0))
        top.pack_propagate(False)
        tk.Label(top, text=title, bg=MATTE_BLACK, fg=MILKY_WHITE, font=("Tahoma", 22, "bold")).pack(side="left", pady=15)
        tk.Label(top, text=subtitle, bg=MATTE_BLACK, fg=OCEAN_BLUE, font=("Tahoma", 9)).pack(side="right", pady=22)

    def stat_card(self, parent, title, value, accent):
        card = tk.Frame(parent, bg=CARD, highlightbackground=accent, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=5, ipady=13)
        tk.Label(card, text=title, bg=CARD, fg=MUTED, font=("Tahoma", 10)).pack(anchor="w", padx=17)
        tk.Label(card, text=str(value), bg=CARD, fg=MILKY_WHITE, font=("Segoe UI", 19, "bold")).pack(anchor="w", padx=17, pady=(4, 0))

    def show_dashboard_page(self):
        self.page_header("داشبورد مدیریت", "مدیریت حرفه‌ای خودرو و تعمیرگاه")
        counts = dashboard_counts()
        stats = tk.Frame(self.content, bg=MATTE_BLACK)
        stats.pack(fill="x", padx=28)
        self.stat_card(stats, "🚘 خودروها", counts["cars"], BLOOD_RED)
        self.stat_card(stats, "👤 مشتریان", counts["customers"], OCEAN_BLUE)
        self.stat_card(stats, "🔧 تعمیرات", counts["services"], BLOOD_RED)
        self.stat_card(stats, "💰 درآمد پرداخت‌شده", f'{counts["income"]:,.0f} تومان', OCEAN_BLUE)
        hero = tk.Frame(self.content, bg=CARD, highlightbackground=OCEAN_BLUE, highlightthickness=1)
        hero.pack(fill="both", expand=True, padx=33, pady=20)
        tk.Label(hero, text="خودروی منتخب", bg=CARD, fg=MILKY_WHITE, font=("Tahoma", 17, "bold")).pack(anchor="e", padx=28, pady=(25, 5))
        tk.Label(hero, text="🚘", bg=CARD, fg=MILKY_WHITE, font=("Segoe UI Emoji", 75)).pack(pady=(35, 5))
        tk.Label(hero, text="از منوی سمت راست خودروها را ثبت کنید؛ تصویر خودرو نیز در پرونده آن ذخیره می‌شود.", bg=CARD, fg=MUTED, font=("Tahoma", 11)).pack()
        tk.Label(hero, text="مشکی مات  •  قرمز خونی  •  آبی اقیانوسی  •  سفید شیری", bg=CARD, fg=OCEAN_BLUE, font=("Tahoma", 9)).pack(pady=15)

    def table_page(self, title, columns, rows, add_command=None, delete_command=None, refresh_command=None):
        self.page_header(title, "AutoMaster Pro")
        bar = tk.Frame(self.content, bg=MATTE_BLACK)
        bar.pack(fill="x", padx=28, pady=(0, 12))
        if add_command:
            tk.Button(bar, text="＋ ثبت مورد جدید", command=add_command, bg=BLOOD_RED, fg=MILKY_WHITE, bd=0, cursor="hand2", font=("Tahoma", 10, "bold"), padx=18, pady=9).pack(side="left", padx=3)
        if delete_command:
            tk.Button(bar, text="🗑 حذف انتخاب‌شده", command=delete_command, bg="#333333", fg=MILKY_WHITE, bd=0, cursor="hand2", font=("Tahoma", 10), padx=15, pady=9).pack(side="left", padx=3)
        if refresh_command:
            tk.Button(bar, text="↻ بروزرسانی", command=refresh_command, bg=OCEAN_BLUE, fg=MILKY_WHITE, bd=0, cursor="hand2", font=("Tahoma", 10), padx=15, pady=9).pack(side="left", padx=3)
        holder = tk.Frame(self.content, bg=CARD)
        holder.pack(fill="both", expand=True, padx=28, pady=(0, 25))
        tree = ttk.Treeview(holder, columns=columns, show="headings")
        for col, heading in columns.items():
            tree.heading(col, text=heading)
            tree.column(col, width=130, anchor="center")
        scroll = ttk.Scrollbar(holder, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scroll.pack(side="right", fill="y", pady=5)
        for row in rows:
            tree.insert("", "end", values=row)
        return tree

    def show_customers(self):
        def load():
            with get_connection() as c:
                return c.execute("SELECT id,name,phone,address,created_at FROM customers ORDER BY id DESC").fetchall()
        def add(): self.customer_form(refresh)
        def delete():
            item = tree.selection()
            if not item: return
            cid = tree.item(item[0])["values"][0]
            if messagebox.askyesno("حذف", "این مشتری حذف شود؟"):
                with get_connection() as c: c.execute("DELETE FROM customers WHERE id=?", (cid,))
                refresh()
        def refresh():
            nonlocal tree
            rows = load()
            tree = self.table_page("مدیریت مشتریان", {"id":"شناسه","name":"نام","phone":"تلفن","address":"آدرس","created":"تاریخ ثبت"}, [tuple(r) for r in rows], add, delete, refresh)
        tree = None
        refresh()

    def customer_form(self, callback):
        win = self.form_window("ثبت مشتری", 430, 330)
        entries = self.labeled_entries(win, [("نام مشتری", "name"), ("شماره تماس", "phone"), ("آدرس", "address")])
        def save():
            if not entries["name"].get().strip(): return messagebox.showwarning("هشدار", "نام مشتری الزامی است.")
            with get_connection() as c: c.execute("INSERT INTO customers(name,phone,address) VALUES(?,?,?)", tuple(entries[k].get().strip() for k in ("name","phone","address")))
            win.destroy(); callback()
        self.save_button(win, save)

    def show_mechanics(self):
        def load():
            with get_connection() as c: return c.execute("SELECT id,name,phone,specialty,created_at FROM mechanics ORDER BY id DESC").fetchall()
        def refresh():
            nonlocal tree
            tree = self.table_page("مدیریت مکانیک‌ها", {"id":"شناسه","name":"نام","phone":"تلفن","specialty":"تخصص","created":"تاریخ"}, [tuple(r) for r in load()], lambda: self.mechanic_form(refresh), delete, refresh)
        def delete():
            if tree and tree.selection():
                mid=tree.item(tree.selection()[0])["values"][0]
                if messagebox.askyesno("حذف", "مکانیک حذف شود?"):
                    with get_connection() as c:c.execute("DELETE FROM mechanics WHERE id=?",(mid,))
                    refresh()
        tree=None; refresh()

    def mechanic_form(self, callback):
        win=self.form_window("ثبت مکانیک",430,330)
        e=self.labeled_entries(win,[("نام مکانیک","name"),("شماره تماس","phone"),("تخصص","specialty")])
        def save():
            if not e["name"].get().strip(): return messagebox.showwarning("هشدار","نام الزامی است.")
            with get_connection() as c:c.execute("INSERT INTO mechanics(name,phone,specialty) VALUES(?,?,?)",(e["name"].get().strip(),e["phone"].get().strip(),e["specialty"].get().strip()))
            win.destroy();callback()
        self.save_button(win,save)

    def show_parts(self):
        def load():
            with get_connection() as c:return c.execute("SELECT id,name,part_number,quantity,price,created_at FROM parts ORDER BY id DESC").fetchall()
        def refresh():
            nonlocal tree
            tree=self.table_page("مدیریت قطعات",{"id":"شناسه","name":"نام قطعه","part_number":"شماره قطعه","quantity":"موجودی","price":"قیمت","created":"تاریخ"},[tuple(r) for r in load()],lambda:self.part_form(refresh),delete,refresh)
        def delete():
            if tree and tree.selection():
                pid=tree.item(tree.selection()[0])["values"][0]
                if messagebox.askyesno("حذف","قطعه حذف شود؟"):
                    with get_connection() as c:c.execute("DELETE FROM parts WHERE id=?",(pid,))
                    refresh()
        tree=None;refresh()

    def part_form(self,callback):
        win=self.form_window("ثبت قطعه",450,390)
        e=self.labeled_entries(win,[("نام قطعه","name"),("شماره قطعه","part_number"),("موجودی","quantity"),("قیمت","price")])
        def save():
            try:q=int(e["quantity"].get() or 0);p=float(e["price"].get() or 0)
            except ValueError:return messagebox.showerror("خطا","موجودی و قیمت باید عددی باشند.")
            if not e["name"].get().strip():return messagebox.showwarning("هشدار","نام قطعه الزامی است.")
            with get_connection() as c:c.execute("INSERT INTO parts(name,part_number,quantity,price) VALUES(?,?,?,?)",(e["name"].get().strip(),e["part_number"].get().strip(),q,p))
            win.destroy();callback()
        self.save_button(win,save)

    def show_cars(self):
        def load():
            with get_connection() as c:return c.execute("SELECT cars.id,cars.name,cars.brand,cars.model,cars.year,cars.color,cars.plate,COALESCE(customers.name,'-'),COALESCE(cars.image_path,'-') FROM cars LEFT JOIN customers ON customers.id=cars.owner_id ORDER BY cars.id DESC").fetchall()
        def refresh():
            nonlocal tree
            tree=self.table_page("مدیریت خودروها",{"id":"شناسه","name":"نام خودرو","brand":"برند","model":"مدل","year":"سال","color":"رنگ","plate":"پلاک","owner":"مالک","image":"تصویر"},[tuple(r) for r in load()],lambda:self.car_form(refresh),delete,refresh)
        def delete():
            if tree and tree.selection():
                cid=tree.item(tree.selection()[0])["values"][0]
                if messagebox.askyesno("حذف","خودرو حذف شود؟"):
                    with get_connection() as c:c.execute("DELETE FROM cars WHERE id=?",(cid,))
                    refresh()
        tree=None;refresh()

    def car_form(self,callback):
        win=self.form_window("ثبت خودرو",520,650)
        fields=[("نام خودرو","name"),("برند","brand"),("مدل","model"),("سال ساخت","year"),("رنگ","color"),("پلاک","plate")]
        e=self.labeled_entries(win,fields)
        with get_connection() as c: owners=c.execute("SELECT id,name FROM customers ORDER BY name").fetchall()
        tk.Label(win,text="مالک",bg=CARD,fg=MILKY_WHITE,font=("Tahoma",10,"bold")).pack(anchor="e",padx=35,pady=(7,2))
        owner=tk.StringVar()
        combo=ttk.Combobox(win,textvariable=owner,state="readonly",justify="right",values=[f"{r['id']} - {r['name']}" for r in owners])
        combo.pack(fill="x",padx=35,ipady=6)
        image_path=tk.StringVar()
        row=tk.Frame(win,bg=CARD);row.pack(fill="x",padx=35,pady=12)
        tk.Entry(row,textvariable=image_path,bg=FIELD,fg=MILKY_WHITE,relief="flat",justify="left").pack(side="left",fill="x",expand=True,ipady=7)
        tk.Button(row,text="انتخاب تصویر",command=lambda:image_path.set(filedialog.askopenfilename(title="انتخاب عکس خودرو",filetypes=[("Images","*.png *.gif *.ppm"),("All files","*.*")])),bg=OCEAN_BLUE,fg=MILKY_WHITE,bd=0,padx=10,pady=7).pack(side="right",padx=(8,0))
        tk.Label(win,text="مسیر تصویر خودرو در دیتابیس ذخیره می‌شود.",bg=CARD,fg=MUTED,font=("Tahoma",8)).pack(anchor="e",padx=35)
        def save():
            try:year=int(e["year"].get()) if e["year"].get().strip() else None
            except ValueError:return messagebox.showerror("خطا","سال ساخت باید عددی باشد.")
            if not e["name"].get().strip():return messagebox.showwarning("هشدار","نام خودرو الزامی است.")
            oid=int(owner.get().split(" - ")[0]) if owner.get() else None
            with get_connection() as c:c.execute("INSERT INTO cars(name,brand,model,year,color,plate,owner_id,image_path) VALUES(?,?,?,?,?,?,?,?)",(e["name"].get().strip(),e["brand"].get().strip(),e["model"].get().strip(),year,e["color"].get().strip(),e["plate"].get().strip(),oid,image_path.get().strip()))
            win.destroy();callback()
        self.save_button(win,save)

    def show_services(self):
        def load():
            with get_connection() as c:return c.execute("SELECT s.id,COALESCE(c.name,'-'),COALESCE(m.name,'-'),s.title,s.cost,s.service_date,s.status FROM services s LEFT JOIN cars c ON c.id=s.car_id LEFT JOIN mechanics m ON m.id=s.mechanic_id ORDER BY s.id DESC").fetchall()
        def refresh():
            nonlocal tree
            tree=self.table_page("مدیریت تعمیرات",{"id":"شناسه","car":"خودرو","mechanic":"مکانیک","title":"خدمت","cost":"هزینه","date":"تاریخ","status":"وضعیت"},[tuple(r) for r in load()],lambda:self.service_form(refresh),delete,refresh)
        def delete():
            if tree and tree.selection():
                sid=tree.item(tree.selection()[0])["values"][0]
                if messagebox.askyesno("حذف","رکورد تعمیرات حذف شود؟"):
                    with get_connection() as c:c.execute("DELETE FROM services WHERE id=?",(sid,))
                    refresh()
        tree=None;refresh()

    def service_form(self,callback):
        win=self.form_window("ثبت تعمیرات",520,620)
        with get_connection() as c:
            cars=c.execute("SELECT id,name FROM cars ORDER BY name").fetchall(); mechs=c.execute("SELECT id,name FROM mechanics ORDER BY name").fetchall()
        def combo(label,values):
            tk.Label(win,text=label,bg=CARD,fg=MILKY_WHITE,font=("Tahoma",10,"bold")).pack(anchor="e",padx=35,pady=(8,2))
            var=tk.StringVar(); cb=ttk.Combobox(win,textvariable=var,state="readonly",justify="right",values=[f"{r['id']} - {r['name']}" for r in values]);cb.pack(fill="x",padx=35,ipady=6);return var
        car=combo("خودرو",cars); mech=combo("مکانیک",mechs)
        e=self.labeled_entries(win,[("عنوان تعمیر","title"),("شرح","description"),("هزینه","cost"),("تاریخ","service_date")])
        status=tk.StringVar(value="pending");tk.Label(win,text="وضعیت",bg=CARD,fg=MILKY_WHITE,font=("Tahoma",10,"bold")).pack(anchor="e",padx=35,pady=(7,2));ttk.Combobox(win,textvariable=status,state="readonly",values=["pending","in_progress","completed"],justify="right").pack(fill="x",padx=35,ipady=6)
        def save():
            try:cost=float(e["cost"].get() or 0)
            except ValueError:return messagebox.showerror("خطا","هزینه باید عددی باشد.")
            cid=int(car.get().split(" - ")[0]) if car.get() else None;mid=int(mech.get().split(" - ")[0]) if mech.get() else None
            if not e["title"].get().strip():return messagebox.showwarning("هشدار","عنوان تعمیر الزامی است.")
            with get_connection() as c:c.execute("INSERT INTO services(car_id,mechanic_id,title,description,cost,service_date,status) VALUES(?,?,?,?,?,?,?)",(cid,mid,e["title"].get().strip(),e["description"].get().strip(),cost,e["service_date"].get().strip(),status.get()))
            win.destroy();callback()
        self.save_button(win,save)

    def show_invoices(self):
        def load():
            with get_connection() as c:return c.execute("SELECT i.id,COALESCE(cu.name,'-'),COALESCE(c.name,'-'),i.total,i.status,i.invoice_date FROM invoices i LEFT JOIN customers cu ON cu.id=i.customer_id LEFT JOIN cars c ON c.id=i.car_id ORDER BY i.id DESC").fetchall()
        def refresh():
            nonlocal tree
            tree=self.table_page("مدیریت فاکتورها",{"id":"شماره","customer":"مشتری","car":"خودرو","total":"مبلغ","status":"وضعیت","date":"تاریخ"},[tuple(r) for r in load()],lambda:self.invoice_form(refresh),delete,refresh)
        def delete():
            if tree and tree.selection():
                iid=tree.item(tree.selection()[0])["values"][0]
                if messagebox.askyesno("حذف","فاکتور حذف شود؟"):
                    with get_connection() as c:c.execute("DELETE FROM invoices WHERE id=?",(iid,))
                    refresh()
        tree=None;refresh()

    def invoice_form(self,callback):
        win=self.form_window("ثبت فاکتور",500,470)
        with get_connection() as c: customers=c.execute("SELECT id,name FROM customers ORDER BY name").fetchall();cars=c.execute("SELECT id,name FROM cars ORDER BY name").fetchall()
        def combo(label,values):
            tk.Label(win,text=label,bg=CARD,fg=MILKY_WHITE,font=("Tahoma",10,"bold")).pack(anchor="e",padx=35,pady=(8,2));var=tk.StringVar();ttk.Combobox(win,textvariable=var,state="readonly",values=[f"{r['id']} - {r['name']}" for r in values],justify="right").pack(fill="x",padx=35,ipady=6);return var
        customer=combo("مشتری",customers);car=combo("خودرو",cars)
        e=self.labeled_entries(win,[("مبلغ کل","total"),("تاریخ","invoice_date")])
        status=tk.StringVar(value="unpaid");tk.Label(win,text="وضعیت پرداخت",bg=CARD,fg=MILKY_WHITE,font=("Tahoma",10,"bold")).pack(anchor="e",padx=35,pady=(8,2));ttk.Combobox(win,textvariable=status,state="readonly",values=["unpaid","paid"],justify="right").pack(fill="x",padx=35,ipady=6)
        def save():
            try:total=float(e["total"].get() or 0)
            except ValueError:return messagebox.showerror("خطا","مبلغ باید عددی باشد.")
            cid=int(customer.get().split(" - ")[0]) if customer.get() else None;carid=int(car.get().split(" - ")[0]) if car.get() else None
            with get_connection() as c:c.execute("INSERT INTO invoices(customer_id,car_id,total,status,invoice_date) VALUES(?,?,?,?,?)",(cid,carid,total,status.get(),e["invoice_date"].get().strip() or None))
            win.destroy();callback()
        self.save_button(win,save)

    def show_users(self):
        def load():
            with get_connection() as c:return c.execute("SELECT id,username,role,created_at FROM users ORDER BY id DESC").fetchall()
        def refresh():
            nonlocal tree
            tree=self.table_page("مدیریت کاربران",{"id":"شناسه","username":"نام کاربری","role":"نقش","created":"تاریخ"},[tuple(r) for r in load()],lambda:self.user_form(refresh),delete,refresh)
        def delete():
            if tree and tree.selection():
                uid=tree.item(tree.selection()[0])["values"][0]
                if str(uid)==str(self.current_user["id"]):return messagebox.showwarning("هشدار","کاربر فعلی قابل حذف نیست.")
                if messagebox.askyesno("حذف","کاربر حذف شود؟"):
                    with get_connection() as c:c.execute("DELETE FROM users WHERE id=?",(uid,))
                    refresh()
        tree=None;refresh()

    def user_form(self,callback):
        win=self.form_window("ثبت کاربر",450,380)
        e=self.labeled_entries(win,[("نام کاربری","username"),("رمز عبور","password")])
        tk.Label(win,text="نقش",bg=CARD,fg=MILKY_WHITE,font=("Tahoma",10,"bold")).pack(anchor="e",padx=35,pady=(8,2));role=tk.StringVar(value="user");ttk.Combobox(win,textvariable=role,state="readonly",values=["user","admin"],justify="right").pack(fill="x",padx=35,ipady=6)
        def save():
            try:
                with get_connection() as c:c.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)",(e["username"].get().strip(),e["password"].get(),role.get()))
            except Exception as ex:return messagebox.showerror("خطا",f"ثبت کاربر انجام نشد.\n{ex}")
            win.destroy();callback()
        self.save_button(win,save)

    def show_reports(self):
        self.page_header("گزارش‌ها و آمار", "گزارش مدیریتی AutoMaster Pro")
        with get_connection() as c:
            paid=c.execute("SELECT COALESCE(SUM(total),0) FROM invoices WHERE status='paid'").fetchone()[0]
            unpaid=c.execute("SELECT COALESCE(SUM(total),0) FROM invoices WHERE status='unpaid'").fetchone()[0]
            services=c.execute("SELECT COALESCE(SUM(cost),0) FROM services").fetchone()[0]
            top=c.execute("SELECT c.name,COUNT(s.id) n FROM cars c LEFT JOIN services s ON s.car_id=c.id GROUP BY c.id ORDER BY n DESC LIMIT 5").fetchall()
        box=tk.Frame(self.content,bg=CARD,highlightbackground=OCEAN_BLUE,highlightthickness=1);box.pack(fill="both",expand=True,padx=28,pady=5)
        data=[("درآمد پرداخت‌شده",f"{paid:,.0f} تومان"),("فاکتورهای پرداخت‌نشده",f"{unpaid:,.0f} تومان"),("مجموع هزینه تعمیرات",f"{services:,.0f} تومان")]
        for title,value in data:
            row=tk.Frame(box,bg=CARD);row.pack(fill="x",padx=35,pady=14);tk.Label(row,text=value,bg=CARD,fg=OCEAN_BLUE,font=("Segoe UI",16,"bold")).pack(side="left");tk.Label(row,text=title,bg=CARD,fg=MILKY_WHITE,font=("Tahoma",12,"bold")).pack(side="right")
        tk.Label(box,text="خودروهای پرتکرار در تعمیرگاه",bg=CARD,fg=MILKY_WHITE,font=("Tahoma",13,"bold")).pack(anchor="e",padx=35,pady=(25,8))
        for r in top:tk.Label(box,text=f"{r['name']}  —  {r['n']} سرویس",bg=CARD,fg=MUTED,font=("Tahoma",10)).pack(anchor="e",padx=45,pady=3)

    def show_settings(self):
        self.page_header("تنظیمات", "تنظیمات سیستم")
        box=tk.Frame(self.content,bg=CARD,highlightbackground=OCEAN_BLUE,highlightthickness=1);box.pack(fill="both",expand=True,padx=28,pady=5)
        settings=[("نام برنامه","AutoMaster Pro"),("رنگ اصلی","مشکی مات + قرمز خونی + آبی اقیانوسی + سفید شیری"),("دیتابیس","SQLite"),("کاربر واردشده",self.current_user.get("username","-")),("سطح دسترسی",self.current_user.get("role","user")),("شماره شاسی (VIN)","در سیستم وجود ندارد")]
        for k,v in settings:
            row=tk.Frame(box,bg=CARD);row.pack(fill="x",padx=35,pady=10);tk.Label(row,text=v,bg=CARD,fg=OCEAN_BLUE,font=("Tahoma",10)).pack(side="left");tk.Label(row,text=k,bg=CARD,fg=MILKY_WHITE,font=("Tahoma",10,"bold")).pack(side="right")

    def form_window(self,title,width,height):
        win=tk.Toplevel(self.root);win.title(title);win.geometry(f"{width}x{height}");win.configure(bg=CARD);win.transient(self.root);win.grab_set();return win

    def labeled_entries(self,win,fields):
        result={}
        for label,key in fields:
            tk.Label(win,text=label,bg=CARD,fg=MILKY_WHITE,font=("Tahoma",10,"bold")).pack(anchor="e",padx=35,pady=(6,2))
            ent=tk.Entry(win,bg=FIELD,fg=MILKY_WHITE,insertbackground=MILKY_WHITE,relief="flat",justify="right",font=("Tahoma",10));ent.pack(fill="x",padx=35,ipady=7);result[key]=ent
        return result

    def save_button(self,win,command):
        tk.Button(win,text="ذخیره اطلاعات",command=command,bg=BLOOD_RED,fg=MILKY_WHITE,activebackground=OCEAN_BLUE,bd=0,cursor="hand2",font=("Tahoma",11,"bold"),pady=10).pack(fill="x",padx=35,pady=20)


def run():
    root=tk.Tk();AutoMasterApp(root);root.mainloop()
