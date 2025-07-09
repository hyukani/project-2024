import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
import psycopg2

# Konfigurasi Database
db_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'berthdb1',
    'user': 'admin',
    'password': 'admin'
}

def connect_db():
    return psycopg2.connect(**db_config)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SiLaju")
        self.geometry("1000x600")
        self.resizable(False, False)

        # Load data schedule dari DB
        self.schedule_data = self.load_schedules_from_db()

        # "Database" sederhana untuk login
        self.users = {}
        self.users["user"] = {"name": "user", "email": "user", "password": "user"}

        self.logged_in_user = None
        self.bookings = []  # Riwayat pemesanan user
        self.last_booking = None  # Simpan booking terakhir
        self.selected_route = None

        # Inisialisasi semua frame
        self.login_frame = LoginFrame(self)
        self.signup_frame = SignUpFrame(self)
        self.home_frame = HomeFrame(self)
        self.route_detail_frame = RouteDetailFrame(self)
        self.customer_data_frame = CustomerDataFrame(self)
        self.payment_method_frame = PaymentMethodFrame(self)
        self.payment_detail_frame = PaymentDetailFrame(self)
        self.history_frame = BookingHistoryFrame(self)
        self.schedule_frame = ScheduleFrame(self)
        self.eticket_frame = ETicketFrame(self)

        self.show_login()

    def load_schedules_from_db(self):
        data = {}
        try:
            conn = connect_db()
            cur = conn.cursor()
            
            query = """
            SELECT s.id_schedule, s.day, s.dep_time, k.nama_kapal, k.asal, k.tujuan, kk.jenis_kelas, kk.harga
            FROM schedule s
            JOIN kapal k ON s.id_kapal = k.id_kapal
            JOIN kelas kk ON s.id_kelas = kk.id_kelas
            """
            cur.execute(query)
            rows = cur.fetchall()

            # Struktur data:
            # data[origin][destination][day] = list of {
            #    "id_schedule": ...,
            #    "day": ...,
            #    "dep_time": ...,
            #    "ship": ...,
            #    "class": ...,
            #    "price": ...
            # }
            for r in rows:
                id_schedule, day, dep_time, nama_kapal, asal, tujuan, jenis_kelas, harga = r
                origin = asal.lower()
                dest = tujuan.lower()
                # Pastikan dep_time jadi string
                dep_time = str(dep_time)

                if origin not in data:
                    data[origin] = {}
                if dest not in data[origin]:
                    data[origin][dest] = {}
                if day not in data[origin][dest]:
                    data[origin][dest][day] = []

                data[origin][dest][day].append({
                    "id_schedule": id_schedule,
                    "day": day,
                    "dep_time": dep_time,
                    "ship": nama_kapal,
                    "class": jenis_kelas,
                    "price": harga
                })

            cur.close()
            conn.close()
        except Exception as e:
            print("Error fetching schedules:", e)
        return data

    def show_login(self):
        self.clear_frames()
        self.login_frame.pack(fill='both', expand=True)

    def show_signup(self):
        self.clear_frames()
        self.signup_frame.pack(fill='both', expand=True)

    def show_home(self):
        self.clear_frames()
        if self.logged_in_user is None:
            self.show_login()
            return
        # Refresh data schedule jika diperlukan
        self.schedule_data = self.load_schedules_from_db()
        self.home_frame.refresh_data(self.schedule_data)
        self.home_frame.pack(fill='both', expand=True)

    def show_schedule(self):
        self.clear_frames()
        self.schedule_frame.refresh_data()
        self.schedule_frame.pack(fill='both', expand=True)

    def show_route_detail(self):
        self.clear_frames()
        self.route_detail_frame.update_info(self.selected_route)
        self.route_detail_frame.pack(fill='both', expand=True)

    def show_customer_data(self):
        self.clear_frames()
        self.customer_data_frame.update_ticket_info(self.selected_route)
        self.customer_data_frame.pack(fill='both', expand=True)

    def show_payment_method(self):
        self.clear_frames()
        self.payment_method_frame.pack(fill='both', expand=True)

    def show_payment_detail(self):
        self.clear_frames()
        self.payment_detail_frame.update_info(self.selected_route)
        self.payment_detail_frame.pack(fill='both', expand=True)

    def show_history(self):
        self.clear_frames()
        self.history_frame.refresh_history(self.bookings)
        self.history_frame.pack(fill='both', expand=True)

    def show_eticket(self):
        self.clear_frames()
        self.eticket_frame.update_info(self.last_booking)
        self.eticket_frame.pack(fill='both', expand=True)

    def clear_frames(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.home_frame.pack_forget()
        self.route_detail_frame.pack_forget()
        self.customer_data_frame.pack_forget()
        self.payment_method_frame.pack_forget()
        self.payment_detail_frame.pack_forget()
        self.history_frame.pack_forget()
        self.schedule_frame.pack_forget()
        self.eticket_frame.pack_forget()

    def add_booking(self, booking_info):
        self.bookings.append(booking_info)
        self.last_booking = booking_info


class SignUpFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        title_font = tkfont.Font(family='Arial', size=14, weight="bold")
        normal_font = tkfont.Font(family='Arial', size=10)

        tk.Label(self, text="Sign Up", bg="white", font=title_font).pack(pady=20)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name", bg="white", font=normal_font).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=1, column=0, sticky="we", padx=5, pady=5)

        tk.Label(form_frame, text="Email", bg="white", font=normal_font).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=1, column=1, sticky="we", padx=5, pady=5)

        tk.Label(form_frame, text="Password", bg="white", font=normal_font).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = tk.Entry(form_frame, show="*")
        self.password_entry.grid(row=3, column=0, sticky="we", padx=5, pady=5)

        tk.Label(form_frame, text="Confirm Password", bg="white", font=normal_font).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.conf_password_entry = tk.Entry(form_frame, show="*")
        self.conf_password_entry.grid(row=3, column=1, sticky="we", padx=5, pady=5)

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        tk.Button(self, text="Sign Up", bg="#0c3866", fg="white", font=normal_font, command=self.sign_up_action).pack(pady=20)
        tk.Button(self, text="Back to Login", bg="white", command=self.go_login).pack()

    def sign_up_action(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip().lower()
        pwd = self.password_entry.get().strip()
        conf = self.conf_password_entry.get().strip()

        if not name or not email or not pwd:
            messagebox.showerror("Error", "All fields are required")
            return

        if pwd != conf:
            messagebox.showerror("Error", "Password and Confirm Password do not match")
            return

        if email in self.master.users:
            messagebox.showerror("Error", "Email already registered")
            return

        self.master.users[email] = {"name": name, "email": email, "password": pwd}
        messagebox.showinfo("Success", "Sign Up successful! You can now login.")
        self.master.show_login()

    def go_login(self):
        self.master.show_login()


class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        
        try:
            bg_image = Image.open("images/Login Page.png")
            bg_image = bg_image.resize((1000, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            pass

        title_font = tkfont.Font(family='Arial', size=14, weight="bold")
        normal_font = tkfont.Font(family='Arial', size=10)
        small_font = tkfont.Font(family='Arial', size=9)

        login_card = tk.Frame(self, bg="white", bd=2, relief="ridge")
        login_card.place(relx=0.5, rely=0.5, anchor="center", width=300, height=400)

        logo_label = tk.Label(login_card, text="SiLaju", bg="white", fg="#333", font=title_font)
        logo_label.pack(pady=(20, 0))
        
        tagline_label = tk.Label(login_card, text="Easy Ship Booking", bg="white", fg="#666", font=normal_font)
        tagline_label.pack(pady=(5, 10))
        
        fb_button = tk.Button(login_card, text="Facebook", fg="white", bg="#3b5998", relief="flat", font=normal_font)
        fb_button.pack(pady=(0,5), fill="x", padx=20)
        
        google_button = tk.Button(login_card, text="Google", fg="black", bg="#ffffff", relief="groove", font=normal_font)
        google_button.pack(pady=(0,5), fill="x", padx=20)
        
        separator_frame = tk.Frame(login_card, bg="white")
        separator_frame.pack(pady=(5,5), fill="x", padx=20)
        
        tk.Label(separator_frame, text="or", bg="white", fg="#666", font=small_font).pack()

        self.email_entry = tk.Entry(login_card, font=normal_font, fg="#999")
        self.email_placeholder = "ex.myname@gmail.com"
        self.email_entry.insert(0, self.email_placeholder)
        self.email_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.email_entry, self.email_placeholder))
        self.email_entry.pack(pady=(5,5), fill="x", padx=20)
        
        self.password_entry = tk.Entry(login_card, font=normal_font, fg="#999", show="")
        self.password_placeholder = "Enter Password"
        self.password_entry.insert(0, self.password_placeholder)
        self.password_entry.config(show="")
        self.password_entry.bind("<FocusIn>", self.clear_password_placeholder)
        self.password_entry.pack(pady=(5,5), fill="x", padx=20)
        
        forgot_label = tk.Label(login_card, text="Forgot your password?", bg="white", fg="blue", font=small_font, cursor="hand2")
        forgot_label.pack(pady=(0,10))
        
        signin_button = tk.Button(login_card, text="Sign In", fg="white", bg="#fbc02d", relief="flat", font=normal_font, command=self.sign_in)
        signin_button.pack(pady=(10,5), fill="x", padx=20)
        
        signup_frame = tk.Frame(login_card, bg="white")
        signup_frame.pack(pady=(5,10))
        
        tk.Label(signup_frame, text="Don't have an account yet?", bg="white", fg="#666", font=small_font).pack(side="left")
        
        signup_label = tk.Label(signup_frame, text="Sign up now", bg="white", fg="blue", font=small_font, cursor="hand2")
        signup_label.pack(side="left", padx=(5,0))
        signup_label.bind("<Button-1>", lambda e: self.master.show_signup())

    def clear_placeholder(self, entry_widget, placeholder):
        if entry_widget.get() == placeholder:
            entry_widget.delete(0, tk.END)
            entry_widget.config(fg="#333")

    def clear_password_placeholder(self, event):
        if self.password_entry.get() == self.password_placeholder:
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show="*", fg="#333")

    def sign_in(self):
        email = self.email_entry.get().strip().lower()
        pwd = self.password_entry.get().strip()
        if pwd == self.password_placeholder:
            pwd = ""

        user_db = self.master.users.get(email)
        if user_db and user_db["password"] == pwd:
            self.master.logged_in_user = user_db
            self.master.show_home()
        else:
            messagebox.showerror("Error", "Login Failed. Please try again.")


class NavBar(tk.Frame):
    def __init__(self, master, go_back=None):
        super().__init__(master, bg="white", height=50)
        self.go_back = go_back
        self.master = master

        logo_font = tkfont.Font(family='Arial', size=16, weight="bold")
        logo_label = tk.Label(self, text="SiLaju\nEasy Ship Booking", bg="white", font=logo_font)
        logo_label.pack(side="left", padx=20)

        nav_font = tkfont.Font(family='Arial', size=10)
        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(side="right", padx=20)

        home_label = tk.Label(nav_frame, text="Home", bg="white", font=nav_font, cursor="hand2")
        home_label.pack(side="left", padx=10)
        home_label.bind("<Button-1>", lambda e: self.master.master.show_home())

        schedule_label = tk.Label(nav_frame, text="Schedule", bg="white", font=nav_font, cursor="hand2")
        schedule_label.pack(side="left", padx=10)
        schedule_label.bind("<Button-1>", lambda e: self.master.master.show_schedule())

        # History Transaksi
        history_label = tk.Label(nav_frame, text="History Transaksi", bg="white", font=nav_font, cursor="hand2")
        history_label.pack(side="left", padx=10)
        history_label.bind("<Button-1>", lambda e: self.master.master.show_history())

        # Ubah Latest Offers menjadi E-Ticket
        eticket_label = tk.Label(nav_frame, text="E-Ticket", bg="white", font=nav_font, cursor="hand2")
        eticket_label.pack(side="left", padx=10)
        eticket_label.bind("<Button-1>", lambda e: self.master.master.show_eticket())

        tk.Label(nav_frame, text="Contact Us", bg="white", font=nav_font).pack(side="left", padx=10)
        tk.Label(nav_frame, text="ID | EN", bg="white", font=nav_font).pack(side="left", padx=10)

        try:
            profile_image = Image.open("images/accounts_icon.png").resize((30,30), Image.Resampling.LANCZOS)
            self.profile_photo = ImageTk.PhotoImage(profile_image)
            profile_label = tk.Label(nav_frame, image=self.profile_photo, bg="white", cursor="hand2")
        except:
            profile_label = tk.Label(nav_frame, text="User", bg="white", cursor="hand2")
        profile_label.pack(side="left", padx=10)
        profile_label.bind("<Button-1>", self.show_user_info)

        if self.go_back:
            back_button = tk.Button(self, text="<", bg="white", bd=0, font=nav_font, command=self.go_back)
            back_button.place(x=5, y=5)

    def show_user_info(self, event):
        if self.master.master.logged_in_user is None:
            messagebox.showerror("Error", "No user logged in.")
            return
        user = self.master.master.logged_in_user

        info_win = tk.Toplevel(self)
        info_win.title("User Info")
        info_win.geometry("300x200")

        info_frame = tk.Frame(info_win, bg="#e0f7fa")
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title_font = tkfont.Font(family='Arial', size=12, weight="bold")
        normal_font = tkfont.Font(family='Arial', size=10)

        tk.Label(info_frame, text="User Information", bg="#e0f7fa", font=title_font).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(info_frame, text="Name:", bg="#e0f7fa", font=normal_font, anchor="e").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Label(info_frame, text=user['name'], bg="#e0f7fa", font=normal_font, anchor="w").grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(info_frame, text="Email:", bg="#e0f7fa", font=normal_font, anchor="e").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Label(info_frame, text=user['email'], bg="#e0f7fa", font=normal_font, anchor="w").grid(row=2, column=1, sticky="w", padx=5, pady=5)

        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)


class HomeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.data = {}
        self.origin_cb = None
        self.destination_cb = None
        self.day_cb = None
        self.dep_time_cb = None
        self.ship_cb = None
        self.class_cb = None
        self.adults_var = None
        self.children_var = None

        self.navbar = NavBar(self, go_back=None)
        self.navbar.pack(fill="x")

        try:
            bg_header = Image.open("images/Homepage.png").resize((1000, 200), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_header)
            tk.Label(self, image=self.bg_photo, bg="white").pack()
        except:
            tk.Label(self, text="Homepage Header", bg="white").pack()

        self.create_search_form()

    def create_search_form(self):
        title_font = tkfont.Font(family='Arial', size=12, weight="bold", slant="roman")
        normal_font = tkfont.Font(family='Arial', size=10)

        search_frame = tk.Frame(self, bg="#000000", bd=0)
        search_frame.place(x=50, y=120, width=500, height=380)

        tk.Label(search_frame, text="Find Your Trip", bg="black", fg="white", font=title_font).pack(pady=(20,0))
        tk.Label(search_frame, text="Set Your Arrival and Departure Schedule at the Port", bg="black", fg="white", font=normal_font).pack(pady=(0,20))

        form_inside = tk.Frame(search_frame, bg="black")
        form_inside.pack(pady=10)

        # Row 1: Origin & Destination
        tk.Label(form_inside, text="Asal", bg="black", fg="white", font=normal_font).grid(row=0, column=0, sticky="w", padx=5)
        self.origin_cb = ttk.Combobox(form_inside, state="readonly")
        self.origin_cb.set("Pilih Asal")
        self.origin_cb.bind("<<ComboboxSelected>>", self.update_destination_options)
        self.origin_cb.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form_inside, text="Tujuan", bg="black", fg="white", font=normal_font).grid(row=0, column=1, sticky="w", padx=5)
        self.destination_cb = ttk.Combobox(form_inside, state="readonly")
        self.destination_cb.set("Pilih Tujuan")
        self.destination_cb.bind("<<ComboboxSelected>>", self.update_day_options)
        self.destination_cb.grid(row=1, column=1, padx=5, pady=5)

        # Row 2: Day & Departure Time
        tk.Label(form_inside, text="Hari", bg="black", fg="white", font=normal_font).grid(row=2, column=0, sticky="w", padx=5)
        self.day_cb = ttk.Combobox(form_inside, state="readonly")
        self.day_cb.set("Pilih Hari")
        self.day_cb.bind("<<ComboboxSelected>>", self.update_dep_time_options)
        self.day_cb.grid(row=3, column=0, padx=5, pady=5)

        tk.Label(form_inside, text="Waktu Keberangkatan", bg="black", fg="white", font=normal_font).grid(row=2, column=1, sticky="w", padx=5)
        self.dep_time_cb = ttk.Combobox(form_inside, state="readonly")
        self.dep_time_cb.set("Pilih Waktu Keberangkatan")
        self.dep_time_cb.bind("<<ComboboxSelected>>", self.update_ship_options)
        self.dep_time_cb.grid(row=3, column=1, padx=5, pady=5)

        # Row 3: Ship & Class
        tk.Label(form_inside, text="Jenis Kapal", bg="black", fg="white", font=normal_font).grid(row=4, column=0, sticky="w", padx=5)
        self.ship_cb = ttk.Combobox(form_inside, state="readonly")
        self.ship_cb.set("Pilih Kapal")
        self.ship_cb.bind("<<ComboboxSelected>>", self.update_class_options)
        self.ship_cb.grid(row=5, column=0, padx=5, pady=5)

        tk.Label(form_inside, text="Kelas", bg="black", fg="white", font=normal_font).grid(row=4, column=1, sticky="w", padx=5)
        self.class_cb = ttk.Combobox(form_inside, state="readonly")
        self.class_cb.set("Pilih Kelas")
        self.class_cb.grid(row=5, column=1, padx=5, pady=5)

        # Row 4: Adults & Children
        tk.Label(form_inside, text="Dewasa\n(Ages 6 and over)", bg="black", fg="white", font=normal_font).grid(row=6, column=0, sticky="w", padx=5)
        self.adults_var = tk.IntVar(value=1)
        tk.Spinbox(form_inside, from_=0, to=10, textvariable=self.adults_var).grid(row=7, column=0, padx=5, pady=5)

        tk.Label(form_inside, text="Anak-Anak\n(2-5 years old)", bg="black", fg="white", font=normal_font).grid(row=6, column=1, sticky="w", padx=5)
        self.children_var = tk.IntVar(value=0)
        tk.Spinbox(form_inside, from_=0, to=10, textvariable=self.children_var).grid(row=7, column=1, padx=5, pady=5)

        tk.Button(search_frame, text="Find Your Ticket", bg="#92d050", fg="black", font=normal_font, command=self.find_ticket_action).pack(pady=10)
        tk.Button(search_frame, text="Manage My Bookings", bg="black", fg="#92d050", font=normal_font, command=self.master.show_history).pack()

    def refresh_data(self, data):
        self.data = data
        origins = list(set([o.capitalize() for o in data.keys()]))
        self.origin_cb.config(values=origins)
        self.origin_cb.set("Pilih Asal")
        self.destination_cb.set("Pilih Tujuan")
        self.destination_cb.config(values=[])
        self.day_cb.set("Pilih Hari")
        self.day_cb.config(values=[])
        self.dep_time_cb.set("Pilih Waktu Keberangkatan")
        self.dep_time_cb.config(values=[])
        self.ship_cb.set("Pilih Kapal")
        self.ship_cb.config(values=[])
        self.class_cb.set("Pilih Kelas")
        self.class_cb.config(values=[])

    def update_destination_options(self, event):
        origin = self.origin_cb.get().lower()
        if origin in self.data:
            destinations = list(set([d.capitalize() for d in self.data[origin].keys()]))
            self.destination_cb.config(values=destinations)
            self.destination_cb.set("Pilih Tujuan")
        else:
            self.destination_cb.config(values=[])
            self.destination_cb.set("Pilih Tujuan")

        self.day_cb.set("Pilih Hari")
        self.day_cb.config(values=[])
        self.dep_time_cb.set("Pilih Waktu Keberangkatan")
        self.dep_time_cb.config(values=[])
        self.ship_cb.set("Pilih Kapal")
        self.ship_cb.config(values=[])
        self.class_cb.set("Pilih Kelas")
        self.class_cb.config(values=[])

    def update_day_options(self, event):
        origin = self.origin_cb.get().strip().lower()
        dest = self.destination_cb.get().strip().lower()
        if origin in self.data and dest in self.data[origin]:
            days = list(self.data[origin][dest].keys())
            self.day_cb.config(values=days)
            self.day_cb.set("Pilih Hari")
        else:
            self.day_cb.config(values=[])
            self.day_cb.set("Pilih Hari")

        self.dep_time_cb.set("Pilih Waktu Keberangkatan")
        self.dep_time_cb.config(values=[])
        self.ship_cb.set("Pilih Kapal")
        self.ship_cb.config(values=[])
        self.class_cb.set("Pilih Kelas")
        self.class_cb.config(values=[])

    def update_dep_time_options(self, event):
        origin = self.origin_cb.get().strip().lower()
        dest = self.destination_cb.get().strip().lower()
        day = self.day_cb.get().strip()

        dep_times = []
        if origin in self.data and dest in self.data[origin] and day in self.data[origin][dest]:
            for sched in self.data[origin][dest][day]:
                if sched['dep_time'] not in dep_times:
                    dep_times.append(sched['dep_time'])

        self.dep_time_cb.config(values=dep_times)
        self.dep_time_cb.set("Pilih Waktu Keberangkatan")

        self.ship_cb.set("Pilih Kapal")
        self.ship_cb.config(values=[])
        self.class_cb.set("Pilih Kelas")
        self.class_cb.config(values=[])

    def update_ship_options(self, event):
        origin = self.origin_cb.get().strip().lower()
        dest = self.destination_cb.get().strip().lower()
        day = self.day_cb.get().strip()
        dep_time = self.dep_time_cb.get().strip()

        ships = []
        if origin in self.data and dest in self.data[origin] and day in self.data[origin][dest]:
            for sched in self.data[origin][dest][day]:
                if sched['dep_time'] == dep_time:
                    if sched['ship'] not in ships:
                        ships.append(sched['ship'])

        self.ship_cb.config(values=ships)
        self.ship_cb.set("Pilih Kapal")
        self.class_cb.set("Pilih Kelas")
        self.class_cb.config(values=[])

    def update_class_options(self, event):
        origin = self.origin_cb.get().strip().lower()
        dest = self.destination_cb.get().strip().lower()
        day = self.day_cb.get().strip()
        dep_time = self.dep_time_cb.get().strip()
        ship = self.ship_cb.get().strip()

        classes = []
        if origin in self.data and dest in self.data[origin] and day in self.data[origin][dest]:
            for sched in self.data[origin][dest][day]:
                if sched['dep_time'] == dep_time and sched['ship'] == ship:
                    if sched['class'] not in classes:
                        classes.append(sched['class'])

        self.class_cb.config(values=classes)
        self.class_cb.set("Pilih Kelas")

    def find_ticket_action(self):
        origin = self.origin_cb.get().strip().lower()
        dest = self.destination_cb.get().strip().lower()
        day = self.day_cb.get().strip()
        dep_time = self.dep_time_cb.get().strip()
        ship = self.ship_cb.get().strip()
        kelas = self.class_cb.get().strip()
        adults = self.adults_var.get()
        children = self.children_var.get()

        route_available = False
        price = None

        if origin in self.data and dest in self.data[origin] and day in self.data[origin][dest]:
            for sched in self.data[origin][dest][day]:
                if sched['dep_time'] == dep_time and sched['ship'] == ship and sched['class'] == kelas:
                    route_available = True
                    price = sched['price']
                    break

        if not route_available:
            messagebox.showinfo("Info", "Maaf, rute tidak tersedia.")
        else:
            self.master.selected_route = {
                "origin": origin.capitalize(),
                "destination": dest.capitalize(),
                "date": day,
                "line": f"{ship} - {kelas}",
                "adults": adults,
                "children": children,
                "price": price,
                "dep_time": dep_time
            }
            self.master.show_route_detail()


class RouteDetailFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        def back():
            self.master.show_home()

        self.navbar = NavBar(self, go_back=back)
        self.navbar.pack(fill="x")

        try:
            bg_header = Image.open("images/Layanan.png").resize((1000, 200), Image.Resampling.LANCZOS)
            self.bg_header_photo = ImageTk.PhotoImage(bg_header)
            header_label = tk.Label(self, image=self.bg_header_photo, bg="white")
            header_label.pack()
        except:
            tk.Label(self, text="Route Header", bg="white").pack()

        self.route_font = tkfont.Font(family='Arial', size=14, weight="bold")
        self.normal_font = tkfont.Font(family='Arial', size=10)

        self.route_label = tk.Label(self, bg="white", font=self.route_font)
        self.route_label.place(x=50, y=210)

        self.info_label = tk.Label(self, bg="white", fg="#666", font=self.normal_font)
        self.info_label.place(x=50, y=240)

        self.detail_frame = tk.Frame(self, bg="#f8f8f8", bd=0, highlightthickness=1, highlightbackground="#ddd")
        self.detail_frame.place(x=50, y=300, width=900, height=200)

        self.seat_info_label = tk.Label(self.detail_frame, text="", bg="#f8f8f8", font=self.normal_font)
        self.seat_info_label.pack(anchor="w", padx=10, pady=10)

        self.book_ticket_btn = tk.Button(self.detail_frame, text="Book Ticket", bg="#92d050", fg="black", font=self.normal_font, command=self.master.show_customer_data)
        self.book_ticket_btn.pack(anchor="e", padx=10, pady=10)

    def update_info(self, route_info):
        if not route_info:
            return
        route_str = f"{route_info['origin']} → {route_info['destination']}"
        self.route_label.config(text=route_str)
        self.info_label.config(text=f"{route_info['date']} | {route_info['line']} | {route_info['adults']} Adult(s) | {route_info['children']} Children")

        self.seat_info_label.config(text=f"Available Seat (238)\n{route_info['origin']} → {route_info['destination']}\n"
                                         f"Departure Date: {route_info['date']} at {route_info['dep_time']}\n"
                                         f"Shipping Line & Class: {route_info['line']}\n\n"
                                         f"Price: Rp. {route_info['price']}")


class CustomerDataFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        def back():
            self.master.show_route_detail()

        self.navbar = NavBar(self, go_back=back)
        self.navbar.pack(fill="x")

        self.canvas = tk.Canvas(self, borderwidth=0, background="#f0f0f0")
        self.frame_content = tk.Frame(self.canvas, background="#ffffff")
        
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.canvas.create_window((0,0), window=self.frame_content, anchor="nw")
        
        self.frame_content.bind("<Configure>", self.on_frame_configure)
        
        title_font = tkfont.Font(family='Arial', size=12, weight="bold")
        normal_font = tkfont.Font(family='Arial', size=10)

        time_label = tk.Label(self.frame_content, text="Your Time Left : 09 Minutes 39 Seconds", fg="red", bg="white", font=normal_font)
        time_label.pack(pady=10, padx=20, anchor="w")

        cust_label = tk.Label(self.frame_content, text="Customer Data Information", bg="white", font=title_font)
        cust_label.pack(pady=(10,0), padx=20, anchor="w")

        field_frame = tk.Frame(self.frame_content, bg="white")
        field_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(field_frame, text="Name", bg="white", font=normal_font).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(field_frame).grid(row=1, column=0, sticky="we", padx=5, pady=5)

        tk.Label(field_frame, text="Email", bg="white", font=normal_font).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        tk.Entry(field_frame).grid(row=1, column=1, sticky="we", padx=5, pady=5)

        tk.Label(field_frame, text="Phone Number", bg="white", font=normal_font).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(field_frame).grid(row=3, column=0, sticky="we", padx=5, pady=5)

        tk.Label(field_frame, text="Address", bg="white", font=normal_font).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        tk.Text(field_frame, height=4, width=30).grid(row=3, column=1, sticky="we", padx=5, pady=5)

        field_frame.grid_columnconfigure(0, weight=1)
        field_frame.grid_columnconfigure(1, weight=1)

        adult_label1 = tk.Label(self.frame_content, text="Adult Passenger Identity Information - Male (1)", bg="white", font=title_font)
        adult_label1.pack(pady=(20,5), padx=20, anchor="w")

        adult_frame1 = tk.Frame(self.frame_content, bg="white")
        adult_frame1.pack(padx=20, pady=10, fill="x")

        tk.Checkbutton(adult_frame1, text="Customer data is the same as passenger data", bg="white").grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

        tk.Label(adult_frame1, text="Date of Birth", bg="white", font=normal_font).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(adult_frame1).grid(row=2, column=0, sticky="we", padx=5, pady=5)

        tk.Label(adult_frame1, text="Gender", bg="white", font=normal_font).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        g1 = tk.Entry(adult_frame1)
        g1.insert(0, "Male")
        g1.grid(row=2, column=1, sticky="we", padx=5, pady=5)

        adult_frame1.grid_columnconfigure(0, weight=1)
        adult_frame1.grid_columnconfigure(1, weight=1)

        self.ticket_frame = tk.Frame(self.frame_content, bg="white", bd=2, relief="groove")
        self.ticket_frame.place(x=600, y=50, width=350, height=200)

        tk.Label(self.ticket_frame, text="Your Ticket", bg="white", font=title_font).pack(pady=10)
        self.ticket_info_label = tk.Label(self.ticket_frame, text="", bg="white", font=normal_font, justify="left")
        self.ticket_info_label.pack(pady=10)

        terms_var = tk.BooleanVar()
        tk.Checkbutton(self.frame_content, text="I agree to the terms and conditions ...", bg="white", variable=terms_var, wraplength=600, justify="left").pack(pady=(20,5), padx=20, anchor="w")

        book_button = tk.Button(self.frame_content, text="Booking", bg="#0c3866", fg="white", font=normal_font, command=self.book_now_action)
        book_button.pack(pady=(20,20))

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_ticket_info(self, route_info):
        if not route_info:
            return
        info = (f"Rute: {route_info['origin']} → {route_info['destination']}\n"
                f"Tanggal: {route_info['date']}\n"
                f"Jenis Kapal & Kelas: {route_info['line']}\n"
                f"Dewasa: {route_info['adults']} | Anak-Anak: {route_info['children']}\n"
                f"Harga: Rp. {route_info['price']}")
        self.ticket_info_label.config(text=info)

    def book_now_action(self):
        self.master.show_payment_method()


class PaymentMethodFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        def back():
            self.master.show_customer_data()

        navbar = NavBar(self, go_back=back)
        navbar.pack(fill="x")

        title_font = tkfont.Font(family='Arial', size=14, weight="bold")
        subtitle_font = tkfont.Font(family='Arial', size=10)

        tk.Label(self, text="Metode Pembayaran", bg="white", font=title_font).pack(pady=(20,0), anchor="w", padx=20)
        tk.Label(self, text="Pilih Metode Pembayaran(s)", bg="white", font=subtitle_font, fg="#666").pack(pady=(5,20), anchor="w", padx=20)

        self.bank_var = tk.BooleanVar()
        self.retail_var = tk.BooleanVar()
        self.ewallet_var = tk.BooleanVar()

        tk.Checkbutton(self, text="Transfer Bank (BCA/BRI/Permata VA)", bg="white", variable=self.bank_var).pack(anchor="w", padx=20, pady=5)
        tk.Checkbutton(self, text="Retail Outlets (Alfamart/Indomaret)", bg="white", variable=self.retail_var).pack(anchor="w", padx=20, pady=5)
        tk.Checkbutton(self, text="E-Wallets (OVO/GOPAY/DANA)", bg="white", variable=self.ewallet_var).pack(anchor="w", padx=20, pady=5)

        confirm_btn = tk.Button(self, text="Proceed to Payment Detail", bg="#0c3866", fg="white", command=self.go_to_payment_detail)
        confirm_btn.pack(pady=20)

    def go_to_payment_detail(self):
        self.master.show_payment_detail()


class PaymentDetailFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        def back():
            self.master.show_payment_method()

        self.navbar = NavBar(self, go_back=back)
        self.navbar.pack(fill="x")

        self.title_font = tkfont.Font(family='Arial', size=14, weight="bold")
        self.normal_font = tkfont.Font(family='Arial', size=10)

        self.method_label = tk.Label(self, text="Payment Details", bg="white", font=self.title_font)
        self.method_label.pack(pady=20)

        self.detail_label = tk.Label(self, bg="white", font=self.normal_font)
        self.detail_label.pack(anchor="w", padx=20)

        self.total_label = tk.Label(self, bg="white", font=self.normal_font, fg="red")
        self.total_label.pack(pady=20)

        confirm_btn = tk.Button(self, text="Confirm Payment", bg="#0c3866", fg="white", font=self.normal_font, command=self.confirm_payment)
        confirm_btn.pack(pady=20)

        self.eticket_btn = tk.Button(self, text="View E-Ticket", bg="#0c3866", fg="white", font=self.normal_font, command=self.view_eticket)
        self.eticket_btn.pack(pady=10)
        self.eticket_btn.config(state="disabled")

    def update_info(self, route_info):
        if not route_info:
            return
        self.detail_label.config(text=f"Payment Method(s) Selected\nRoute: {route_info['origin']} → {route_info['destination']}\nDate: {route_info['date']}\nShip & Class: {route_info['line']}")
        self.total_label.config(text=f"Total: Rp. {route_info['price']}")

    def confirm_payment(self):
        route_info = self.master.selected_route
        self.master.add_booking({
            "route": f"{route_info['origin']} → {route_info['destination']}",
            "date": route_info["date"],
            "class": route_info["line"],
            "passengers": f"{route_info['adults']} Adult(s), {route_info['children']} Children",
            "price": f"Rp. {route_info['price']}"
        })
        messagebox.showinfo("Success", "Your payment is confirmed! Enjoy your trip.")
        self.eticket_btn.config(state="normal")

    def view_eticket(self):
        self.master.show_eticket()


class BookingHistoryFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        def back():
            self.master.show_home()

        navbar = NavBar(self, go_back=back)
        navbar.pack(fill="x")

        title_font = tkfont.Font(family='Arial', size=14, weight="bold")

        tk.Label(self, text="Booking History", bg="white", font=title_font).pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("route", "date", "class", "passengers", "price"), show="headings")
        self.tree.heading("route", text="Rute")
        self.tree.heading("date", text="Tanggal")
        self.tree.heading("class", text="Kelas")
        self.tree.heading("passengers", text="Penumpang")
        self.tree.heading("price", text="Harga")

        self.tree.pack(pady=10, fill="x", padx=20)

        self.chart_canvas = tk.Canvas(self, bg="white", height=200)
        self.chart_canvas.pack(pady=10, fill="x", padx=20)

    def refresh_history(self, bookings):
        for i in self.tree.get_children():
            self.tree.delete(i)

        route_count = {}
        for b in bookings:
            self.tree.insert("", "end", values=(b['route'], b['date'], b['class'], b['passengers'], b['price']))
            route = b['route']
            route_count[route] = route_count.get(route, 0) + 1

        self.draw_chart(route_count)

    def draw_chart(self, route_count):
        self.chart_canvas.delete("all")
        if not route_count:
            self.chart_canvas.create_text(100,50, text="Tidak ada riwayat pemesanan.", anchor="w")
            return

        x = 50
        max_count = max(route_count.values())
        scale = 100 / max_count

        for route, count in route_count.items():
            bar_height = count * scale
            self.chart_canvas.create_rectangle(x, 150 - bar_height, x+50, 150, fill="#92d050")
            self.chart_canvas.create_text(x+25, 155, text=route, anchor="n", font=("Arial",8))
            self.chart_canvas.create_text(x+25, 150 - bar_height - 10, text=str(count), anchor="s")
            x += 100


class ScheduleFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        def back():
            self.master.show_home()

        self.navbar = NavBar(self, go_back=back)
        self.navbar.pack(fill="x")

        title_font = tkfont.Font(family='Arial', size=14, weight="bold")
        tk.Label(self, text="Schedule Board", bg="white", font=title_font).pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("id_schedule","jenis_kelas","day","dep_time","nama_kapal","asal","tujuan","harga"), show="headings")
        self.tree.heading("id_schedule", text="ID")
        self.tree.heading("jenis_kelas", text="Kelas")
        self.tree.heading("day", text="Hari")
        self.tree.heading("dep_time", text="Waktu Keberangkatan")
        self.tree.heading("nama_kapal", text="Ship Name")
        self.tree.heading("asal", text="Asal Keberangkatan")
        self.tree.heading("tujuan", text="Tujuan Keberangkatan")
        self.tree.heading("harga", text="Harga")

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

    def refresh_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            conn = connect_db()
            cur = conn.cursor()
            query = """
            SELECT s.id_schedule, kk.jenis_kelas, s.day, s.dep_time, k.nama_kapal, k.asal, k.tujuan, kk.harga
            FROM schedule s
            JOIN kapal k ON s.id_kapal = k.id_kapal
            JOIN kelas kk ON s.id_kelas = kk.id_kelas
            """
            cur.execute(query)
            rows = cur.fetchall()
            for r in rows:
                self.tree.insert("", "end", values=r)
            cur.close()
            conn.close()
        except Exception as e:
            print("Error loading schedule:", e)


class ETicketFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        def back():
            self.master.show_home()

        self.navbar = NavBar(self, go_back=back)
        self.navbar.pack(fill="x")

        self.title_font = tkfont.Font(family='Arial', size=14, weight="bold")
        self.normal_font = tkfont.Font(family='Arial', size=10)

        tk.Label(self, text="E-Ticket", bg="white", font=self.title_font).pack(pady=20)

        eticket_frame = tk.Frame(self, bg="#cceeff", bd=2, relief="groove")
        eticket_frame.pack(pady=20, padx=50, fill="x")

        self.info_label = tk.Label(eticket_frame, text="", bg="#cceeff", font=self.normal_font, justify="left")
        self.info_label.pack(pady=20, padx=20, anchor="w")

    def update_info(self, booking):
        if not booking:
            self.info_label.config(text="No e-ticket available.")
            return
        info = (f"Rute: {booking['route']}\n"
                f"Tanggal: {booking['date']}\n"
                f"Line/Kelas: {booking['class']}\n"
                f"Penumpang: {booking['passengers']}\n"
                f"Harga: {booking['price']}\n\n"
                f"*** E-Ticket Anda Sudah Dicetak ***\nHarap Tunjukkan Ke Petugas Sebelum Berangkat")
        self.info_label.config(text=info)
        

if __name__ == "__main__":
    app = Application()
    app.mainloop()
