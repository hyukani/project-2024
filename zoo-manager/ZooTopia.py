from tkinter import *
from tkinter import PhotoImage
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from collections import deque
from datetime import datetime, timedelta
import sqlite3


class ZooTopia:
    def __init__(self, window):
        self.window = window
        window.geometry('1166x718')
        window.state('zoomed')
        window.title('ZooTopia')

        # Background
        self.bg_frame = Image.open("bg 1.png")
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        self.window.after(3000, self.main_page)

        # Initialize map variables
        self.map_img = None
        self.ax = None
        self.fig = None

        # Initialize the database sepeda and the queue
        self.conn = sqlite3.connect('sepeda_orders.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        self.sepeda_queue = deque(maxlen=20)
        self.set_initial_nomor_antrean()

        # Initialize the database perahu and the queue
        self.conn_perahu = sqlite3.connect('perahu_orders.db')
        self.cursor_perahu = self.conn_perahu.cursor()
        self.create_perahu_table()
        self.set_initial_nomor_antrean_perahu()
        self.perahu_queue = []

    #=== DATA BASE ===#
    def create_table(self):
        # Create table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                nomor_antrean INTEGER PRIMARY KEY,
                                nama TEXT,
                                waktu_pemesanan TEXT,
                                waktu_batas_penggunaan TEXT,
                                status TEXT)''')
        self.conn.commit()

    def create_perahu_table(self):
        self.cursor_perahu.execute('''CREATE TABLE IF NOT EXISTS boat_orders (
                                    nomor_antrean INTEGER PRIMARY KEY,
                                    nama TEXT,
                                    jumlah_orang INTEGER,
                                    waktu_pemesanan TEXT)''')
        self.conn_perahu.commit()


    def set_initial_nomor_antrean(self):
        # Get the highest nomor_antrean from the database
        self.cursor.execute('SELECT MAX(nomor_antrean) FROM orders')
        result = self.cursor.fetchone()
        if result[0] is not None:
            self.nomor_antrean = result[0] + 1
        else:
            self.nomor_antrean = 1

    def set_initial_nomor_antrean_perahu(self):
        self.cursor_perahu.execute('SELECT MAX(nomor_antrean) FROM boat_orders')
        result = self.cursor_perahu.fetchone()
        if result[0] is not None:
            self.nomor_antrean_perahu = result[0] + 1
        else:
            self.nomor_antrean_perahu = 1


    def update_status(self):
        # Update status to "tersedia" for orders that have exceeded waktu_batas_penggunaan
        now = datetime.now()
        self.cursor.execute('''UPDATE orders
                               SET status = "tersedia"
                               WHERE status = "terpakai" AND waktu_batas_penggunaan <= ?''',
                            (now,))
        self.conn.commit()


    #=== MAIN PAGE ===#
    def main_page(self):
        # Background
        self.bg_frame = Image.open("bg 2.png")
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel.configure(image=photo)  # Update gambar
        self.bg_panel.image = photo

        # Explore
        # Menggunakan PIL untuk membuka gambar
        explore_image = Image.open("explore.png")
        # Mengonversi gambar menjadi format yang dapat ditampilkan oleh Tkinter
        explore_photo = ImageTk.PhotoImage(explore_image)

        # Menampilkan gambar sebagai label
        img_explore = Label(image=explore_photo)
        img_explore.image = explore_photo  # Simpan referensi ke objek PhotoImage untuk mencegah garbage collection

        # Menampilkan gambar sebagai tombol
        explore_button = Button(self.bg_panel, image=explore_photo, command=self.explore_action, borderwidth=0, cursor='hand2')
        explore_button.place(x=60, y=-10)


        # Satwa
        satwa_image = Image.open("satwa.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(self.bg_panel, image=satwa_photo, command=self.satwa_page, borderwidth=0, cursor='hand2')
        satwa_button.place(x=350, y=-90)

        # Fasilitas
        fasilitas_image = Image.open("fasilitas.png")
        fasilitas_photo = ImageTk.PhotoImage(fasilitas_image)
        img_fasilitas = Label(image=fasilitas_photo)
        img_fasilitas.image = fasilitas_photo
        fasilitas_button = Button(self.bg_panel, image=fasilitas_photo, command=self.fasilitas, borderwidth=0, cursor='hand2')
        fasilitas_button.place(x=630, y=-10)

        # Maps
        maps_image = Image.open("maps.png")
        maps_photo = ImageTk.PhotoImage(maps_image)
        img_maps = Label(image=maps_photo)
        img_maps.image = maps_photo
        maps_button = Button(self.bg_panel, image=maps_photo, command=self.show_map, borderwidth=0, cursor='hand2')
        maps_button.place(x=920, y=-90)

        # Dropdown menu
        self.menu = Menu(self.window, tearoff=0, bg='#ddf4e0', relief=FLAT, activebackground='#ddf4e0')
        self.option1_image = PhotoImage(file="bg 3.png").subsample(2)  # Subsampling gambar menjadi setengah ukuran aslinya
        self.option2_image = PhotoImage(file="bg 4.png").subsample(2)
        self.menu.add_command(compound=NONE, image=self.option1_image, command=self.tiket)
        self.menu.add_command(compound=NONE, image=self.option2_image, command=self.peraturan)

    def explore_action(self):
        # Positioning the menu
        explore_button_x = 80
        explore_button_y = 210
        self.menu.post(explore_button_x, explore_button_y)


    #=== TIKET ===#
    def tiket(self):
        self.tiket_bg = Toplevel()
        self.tiket_bg.geometry('1270x700')
        self.tiket_bg.state('zoomed')
        self.tiket_bg.title('Tiket')

        # Background
        photo_frame = Image.open("tiket.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        self.bg_panel = Label(self.tiket_bg, image=photo_bg)
        self.bg_panel.image = photo_bg
        self.bg_panel.pack(fill='both', expand='yes')


    #=== PERATURAN ===#
    def peraturan(self):
        self.peraturan_bg = Toplevel()
        self.peraturan_bg.geometry('1270x700')
        self.peraturan_bg.state('zoomed')
        self.peraturan_bg.title('Peraturan')

        # Background
        photo_frame = Image.open("peraturan.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        self.bg_panel = Label(self.peraturan_bg, image=photo_bg)
        self.bg_panel.image = photo_bg
        self.bg_panel.pack(fill='both', expand='yes')


    #=== FASILITAS ===#
    def fasilitas(self):
        self.fasilitas_bg = Toplevel()
        self.fasilitas_bg.geometry('1270x700')
        self.fasilitas_bg.state('zoomed')
        self.fasilitas_bg.title('Fasilitas')

        # Buat Notebook
        self.style = ttk.Style()
        self.style.configure('TNotebook', background='#ddf4e0', borderwidth=0)
        self.style.configure('TNotebook.Tab', font=('Elephant', 14), foreground='#092e05')
        self.style.map('TNotebook.Tab', foreground=[('selected', '#092e05')])

        self.notebook = ttk.Notebook(self.fasilitas_bg, style='TNotebook')
        self.notebook.pack(pady=10, fill=tk.BOTH, expand=True)

        # Tab Fasilitas
        self.tab_fasilitas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_fasilitas, text='Fasilitas')
        self.buat_fasilitas(self.tab_fasilitas)

        # Tab Peminjaman Fasilitas
        self.tab_peminjaman = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_peminjaman, text='Peminjaman Fasilitas')
        self.buat_peminjaman(self.tab_peminjaman)

        # Tab Tiket Peminjaman Fasilitas
        self.tab_tiket = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tiket, text='Tiket Peminjaman Fasilitas')
        self.buat_tiket_peminjaman(self.tab_tiket)

    def buat_fasilitas(self, parent):
        # Create a frame to contain all widgets
        main_frame = tk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=tk.YES)

        # Create canvas with scrollbar
        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.config(yscrollcommand=scrollbar.set)

        # Create a frame to contain your images/buttons
        bg_panel = tk.Frame(canvas)
        canvas.create_window((0, 0), window=bg_panel, anchor="nw")

        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Background
        photo_frame = Image.open("fas.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        bg_label = tk.Label(bg_panel, image=photo_bg)
        bg_label.image = photo_bg
        bg_label.pack(fill='both', expand='yes')

    def buat_peminjaman(self, parent):
        # Background
        photo_frame = Image.open("aturan peminjaman.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        self.bg_panel = Label(parent, image=photo_bg)
        self.bg_panel.image = photo_bg
        self.bg_panel.pack(fill='both', expand='yes')

        # Button
        button1_image = Image.open("sepeda.png")
        button1_photo = ImageTk.PhotoImage(button1_image)
        button1 = Button(self.bg_panel, image=button1_photo, command=self.sepeda, borderwidth=0, cursor='hand2')
        button1.image = button1_photo
        button1.place(x=300, y=450)

        button2_image = Image.open("perahu.png")
        button2_photo = ImageTk.PhotoImage(button2_image)
        button2 = Button(self.bg_panel, image=button2_photo, command=self.perahu, borderwidth=0, cursor='hand2')
        button2.image = button2_photo
        button2.place(x=750, y=450)

    def buat_tiket_peminjaman(self, parent) :
        # Background
        photo_frame = Image.open("bg polos.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        self.bg_panel = Label(parent, image=photo_bg)
        self.bg_panel.image = photo_bg
        self.bg_panel.pack(fill='both', expand='yes')

        # Connect to sepeda_orders.db
        self.conn_sepeda = sqlite3.connect('sepeda_orders.db')
        self.cursor_sepeda = self.conn_sepeda.cursor()

        # Get data from sepeda_orders database
        self.cursor_sepeda.execute("SELECT * FROM orders")
        sepeda_orders = self.cursor_sepeda.fetchall()

        # Display sepeda orders
        for order in sepeda_orders:
            try:
                # Parse and adjust the time
                waktu_pemesanan_str = order[2].split('.')[0]  # Remove microseconds
                waktu_pemesanan = datetime.strptime(waktu_pemesanan_str, '%Y-%m-%d %H:%M:%S')
                waktu_mulai = waktu_pemesanan + timedelta(minutes=10)
                waktu_mulai_str = waktu_mulai.strftime('%H:%M')

                # Format waktu_batas_penggunaan tanpa detik
                waktu_batas_penggunaan_str = order[3]
                waktu_batas_penggunaan = datetime.strptime(waktu_batas_penggunaan_str, '%Y-%m-%d %H:%M')
                waktu_batas_str = waktu_batas_penggunaan.strftime('%H:%M')


                order_frame = tk.Frame(self.bg_panel, bd=2, relief="groove")
                order_frame.pack(pady=10, padx=10, fill="x")

                # Create labels to display order information
                tk.Label(order_frame, text=f"Nomor Antrean Sepeda : {order[0]}", font=("Arial", 12, "bold")).pack(anchor="w")
                tk.Label(order_frame, text=f"Nama                               : {order[1]}", font=("Arial", 10)).pack(anchor="w")
                tk.Label(order_frame, text=f"Waktu Mulai                     : {waktu_mulai_str}", font=("Arial", 10)).pack(anchor="w")
                tk.Label(order_frame, text=f"Waktu Batas Penggunaan : {waktu_batas_str}", font=("Arial", 10)).pack(anchor="w")
            except ValueError as e:
                print(f"Error parsing date: {order[2]} - {e}")

        # Close sepeda_orders connection
        self.conn_sepeda.close()

        # Connect to perahu_orders.db
        self.conn_perahu = sqlite3.connect('perahu_orders.db')
        self.cursor_perahu = self.conn_perahu.cursor()

        # Get data from perahu_orders database
        self.cursor_perahu.execute("SELECT * FROM boat_orders")
        perahu_orders = self.cursor_perahu.fetchall()

        # Display perahu orders
        for order in perahu_orders:
            try:
                # Parse and adjust the time
                waktu_pemesanan_str = order[3].split('.')[0]  # Remove microseconds
                waktu_pemesanan = datetime.strptime(waktu_pemesanan_str, '%Y-%m-%d %H:%M:%S')
                waktu_mulai = waktu_pemesanan + timedelta(minutes=10)
                waktu_mulai_str = waktu_mulai.strftime('%H:%M')

                order_frame = tk.Frame(self.bg_panel, bd=2, relief="groove")
                order_frame.pack(pady=10, padx=10, fill="x")

                # Create labels to display order information
                tk.Label(order_frame, text=f"Nomor Antrean Perahu : {order[0]}", font=("Arial", 12, "bold")).pack(anchor="w")
                tk.Label(order_frame, text=f"Nama               : {order[1]}", font=("Arial", 10)).pack(anchor="w")
                tk.Label(order_frame, text=f"Jumlah Orang   : {order[2]}", font=("Arial", 10)).pack(anchor="w")
            except ValueError as e:
                print(f"Error parsing date: {order[3]} - {e}")

    def sepeda(self):
        self.peraturan_bg = Toplevel()
        self.peraturan_bg.geometry('700x500')
        self.peraturan_bg.title('Sepeda')

        # Background
        photo_frame = Image.open("1.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        self.bg_panel = Label(self.peraturan_bg, image=photo_bg)
        self.bg_panel.image = photo_bg
        self.bg_panel.pack(fill='both', expand='yes')

        button3_image = Image.open("3.png")
        button3_photo = ImageTk.PhotoImage(button3_image)
        button2 = Button(self.bg_panel, image=button3_photo, command=self.process_order, borderwidth=0, cursor='hand2')
        button2.image = button3_photo
        button2.place(x=400, y=300)

        # Entry Nama
        bold_font = ("Helvetica", 10, "bold")
        self.nama_entry = Entry(self.bg_panel, width=40, font=bold_font)
        self.nama_entry.place(x=250, y=240)

    def process_order(self):
        # Update status of orders before processing new order
        self.update_status()

        # Dapatkan nama pelanggan dan waktu mulai pesanan dari entry
        nama_pelanggan = self.nama_entry.get()

        # Periksa jumlah sepeda yang sedang terpakai
        self.cursor.execute('SELECT COUNT(*) FROM orders WHERE status = "terpakai"')
        sepeda_terpakai = self.cursor.fetchone()[0]

        if sepeda_terpakai < 20:
            # Tambahkan pesanan ke antrian
            waktu_pemesanan = datetime.now()
            waktu_batas_penggunaan = waktu_pemesanan + timedelta(minutes=40)
            waktu_mulai = (waktu_pemesanan + timedelta(minutes=10)).strftime('%H:%M')
            waktu_batas = waktu_batas_penggunaan.strftime('%H:%M')
            pesanan = {
                'nomor_antrean': self.nomor_antrean,
                'nama': nama_pelanggan,
                'waktu_pemesanan': waktu_pemesanan,
                'waktu_batas_penggunaan': waktu_batas_penggunaan,
                'status': "terpakai"
            }
            self.sepeda_queue.append(pesanan)

            # Simpan pesanan ke database
            try:
                self.cursor.execute('''INSERT INTO orders (nomor_antrean, nama, waktu_pemesanan, waktu_batas_penggunaan, status)
                                       VALUES (?, ?, ?, ?, ?)''',
                                       (self.nomor_antrean, nama_pelanggan, waktu_pemesanan.strftime('%Y-%m-%d %H:%M:%S'),
                                        waktu_batas_penggunaan.strftime('%Y-%m-%d %H:%M'), "terpakai"))
                self.conn.commit()

                # Tampilkan pesan konfirmasi
                messagebox.showinfo("Sukses", f"Pesanan untuk {nama_pelanggan} telah berhasil diterima.\n")

                # Buat jendela Toplevel untuk menampilkan informasi pesanan
                order_info_window = Toplevel(self.peraturan_bg)
                order_info_window.geometry('400x210')
                order_info_window.title("Informasi Pesanan")

                # Mencegah perubahan ukuran dan memaksimalkan jendela
                order_info_window.resizable(False, False)
                # Mengatur posisi jendela Toplevel di tengah layar
                x, y = self.get_window_position(order_info_window)
                order_info_window.geometry(f"+{x}+{y}")

                # Background
                photo_frame = Image.open("info.png")
                photo_bg = ImageTk.PhotoImage(photo_frame)
                self.bg_panel = Label(order_info_window, image=photo_bg)
                self.bg_panel.image = photo_bg
                self.bg_panel.pack(fill='both', expand='yes')

                info_label = Label(self.bg_panel, text= f"Nama                             : {nama_pelanggan}\n"
                                                        f"Nomor Antrean           : {self.nomor_antrean}\n"
                                                        f"Waktu Mulai                 : {waktu_mulai}\n"
                                                        f"Batas Penggunaan    : {waktu_batas}",
                                    bg="#bfffc7",font=("Helvetica", 12, "bold"), anchor="w", justify="left")
                info_label.place(x=60, y=60)

                # Increment nomor antrean untuk pesanan selanjutnya
                self.nomor_antrean += 1
            except sqlite3.IntegrityError:
                messagebox.showerror("Kesalahan", "Gagal menambahkan pesanan. Silakan coba lagi.")

            self.fasilitas_bg.withdraw()

        else:
            # Jika semua sepeda sedang terpakai, tampilkan pesan kesalahan
            messagebox.showerror("Kesalahan", "Semua sepeda sedang terpakai. Silakan tunggu hingga ada sepeda yang tersedia.")

    def return_bike(self, nomor_antrean):
        # Mengubah status pesanan menjadi "tersedia" saat sepeda dikembalikan
        self.cursor.execute('''UPDATE orders SET status = "tersedia" WHERE nomor_antrean = ?''', (nomor_antrean,))
        self.conn.commit()
        messagebox.showinfo("Pengembalian", f"Sepeda dengan nomor antrean {nomor_antrean} telah dikembalikan dan tersedia untuk pemesanan baru.")

    def perahu(self):
        self.peraturan_bg = Toplevel()
        self.peraturan_bg.geometry('700x500')
        self.peraturan_bg.title('Perahu')

        # Background
        photo_frame = Image.open("2.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        self.bg_panel = Label(self.peraturan_bg, image=photo_bg)
        self.bg_panel.image = photo_bg
        self.bg_panel.pack(fill='both', expand='yes')

        button3_image = Image.open("3.png")
        button3_photo = ImageTk.PhotoImage(button3_image)
        button2 = Button(self.bg_panel, image=button3_photo, command=self.process_boat_order, borderwidth=0, cursor='hand2')
        button2.image = button3_photo
        button2.place(x=400, y=350)

        # Entry Nama
        bold_font = ("Helvetica", 10, "bold")
        self.nama_entry2 = Entry(self.bg_panel, width=40, font=bold_font)
        self.nama_entry2.place(x=260, y=235)

        # Combo Box dengan angka-angka
        angka = list(range(1, 11))

        # Membuat style untuk combobox
        style = ttk.Style()
        style.configure("TCombobox", font=bold_font)

        self.combo = ttk.Combobox(self.bg_panel, values=angka, style="TCombobox")
        self.combo.place(x=260, y=270)

        # Event handler untuk combo box
        def on_select(event):
            print(f"Angka yang dipilih: {self.combo.get()}")

        self.combo.bind("<<ComboboxSelected>>", on_select)

    def process_boat_order(self):
        nama_pelanggan = self.nama_entry2.get()
        jumlah_orang = self.combo.get()
        waktu_pemesanan = datetime.now()

        pesanan = {
            'nomor_antrean': self.nomor_antrean_perahu,  # Gunakan nomor antrean perahu yang terpisah
            'nama': nama_pelanggan,
            'jumlah_orang': jumlah_orang,
            'waktu_pemesanan': waktu_pemesanan,
            }
        self.perahu_queue.append(pesanan)

        try:
            self.cursor_perahu.execute('''INSERT INTO boat_orders (nomor_antrean, nama, jumlah_orang, waktu_pemesanan)
                                    VALUES (?, ?, ?, ?)''',
                                    (self.nomor_antrean_perahu, nama_pelanggan, jumlah_orang, waktu_pemesanan))
            self.conn_perahu.commit()

            # Tampilkan pesan konfirmasi
            messagebox.showinfo("Sukses", f"Pesanan untuk {nama_pelanggan} telah berhasil diterima.\n")

        # Buat jendela Toplevel untuk menampilkan informasi pesanan
            order_info_window = Toplevel()
            order_info_window.geometry('400x210')
            order_info_window.title("Informasi Pesanan")

        # Mencegah perubahan ukuran dan memaksimalkan jendela
            order_info_window.resizable(False, False)
        # Mengatur posisi jendela Toplevel di tengah layar
            x, y = self.get_window_position(order_info_window)
            order_info_window.geometry(f"+{x}+{y}")

        # Background
            photo_frame = Image.open("info.png")
            photo_bg = ImageTk.PhotoImage(photo_frame)
            bg_panel = Label(order_info_window, image=photo_bg)
            bg_panel.image = photo_bg
            bg_panel.pack(fill='both', expand='yes')

            info_label = Label(bg_panel, text=  f"Nama                            : {nama_pelanggan}\n"
                                                f"Nomor Antrean           : {self.nomor_antrean_perahu}\n"
                                                f"Jumlah Orang             : {jumlah_orang}",
                                bg="#bfffc7",font=("Helvetica", 12, "bold"), anchor="w", justify="left")
            info_label.place(x=60, y=65)

            self.nomor_antrean_perahu += 1
        except sqlite3.IntegrityError:
            messagebox.showerror("Kesalahan", "Gagal menambahkan pesanan. Silakan coba lagi.")

        self.fasilitas_bg.withdraw()


    #=== MAP ===#
    def show_map(self):
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()

        if self.map_img is None:
            # Memunculkan gambar map
            self.map_img = mpimg.imread('map.png')
            self.fig, self.ax = plt.subplots(figsize=(10, 6))
            self.ax.imshow(self.map_img)
            self.ax.set_axis_off()

            # Show legend
            self.ax.legend()
            self.center_window(self.fig, screen_width, screen_height)
            plt.show()
        else:
            # Menunjukkan map
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(self.map_img)
            ax.set_axis_off()
            self.center_window(fig, screen_width, screen_height)
            plt.show()

    def center_window(self, fig, screen_width, screen_height):
        # Mendapatkan manajer figur untuk mengatur posisi window
        manager = plt.get_current_fig_manager()
        if hasattr(manager, 'window'):
            fig_width, fig_height = fig.get_size_inches() * fig.dpi
            fig_x = (screen_width - fig_width) // 2
            fig_y = (screen_height - fig_height) // 2
            manager.window.wm_geometry(f"{int(fig_width)}x{int(fig_height)}+{int(fig_x)}+{int(fig_y)}")

    #=== SATWA PAGE ===#
    def satwa_page(self):
        self.peraturan_bg = Toplevel()
        self.peraturan_bg.geometry('1270x700')
        self.peraturan_bg.state('zoomed')
        self.peraturan_bg.title('Satwa')

        # Background
        photo_frame = Image.open("bg 5.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        self.bg_panel = Label(self.peraturan_bg, image=photo_bg)
        self.bg_panel.image = photo_bg
        self.bg_panel.pack(fill='both', expand='yes')

        # Canvas for Entry with Image Background
        self.entry_canvas = tk.Canvas(self.bg_panel, width=400, height=60, bd=0, highlightthickness=0)
        self.entry_canvas.place(x=340, y=70)

        # Load image for entry background
        entry_bg_image = Image.open("searching.png")
        entry_bg_image = entry_bg_image.resize((400, 60), Image.BILINEAR)  # Sesuaikan ukuran sesuai kebutuhan
        self.entry_bg_photo = ImageTk.PhotoImage(entry_bg_image)

        # Add background image to canvas
        self.entry_canvas.create_image(0, 0, anchor='nw', image=self.entry_bg_photo)

        # Create entry on top of canvas
        self.search_entry = Entry(self.entry_canvas, width=25, bd=0, highlightthickness=0, font=("Arial", 16))
        self.entry_canvas.create_window(165, 30, window=self.search_entry)  # Center the entry

        # Button
        search_image = Image.open("button search.png")
        search_photo = ImageTk.PhotoImage(search_image)
        img_search = Label(image=search_photo)
        img_search.image = search_photo
        self.search_button = Button(self.bg_panel, image=search_photo, command=self.search, borderwidth=0)
        self.search_button.place(x=750, y=75)

        # Membuat frame
        frame = tk.Frame(self.bg_panel)
        frame.place(x=350, y=145)

        custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Listbox
        self.result_listbox = tk.Listbox(frame, width=60, height=6, font=custom_font)
        self.result_listbox.pack(side="left", fill="y")

        # Membuat Scrollbar
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.result_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_listbox.config(yscrollcommand=scrollbar.set)

        # Gambar
        mamalia_image = Image.open("mamalia.png")
        mamalia_photo = ImageTk.PhotoImage(mamalia_image)
        img_mamalia = Label(image=mamalia_photo)
        img_mamalia.image = mamalia_photo
        mamalia_button = Button(self.bg_panel, image=mamalia_photo, command=self.mamalia, borderwidth=0)
        mamalia_button.place(x=120, y=290)

        pisces_image = Image.open("pisces.png")
        pisces_photo = ImageTk.PhotoImage(pisces_image)
        img_pisces = Label(image=pisces_photo)
        img_pisces.image = pisces_photo
        pisces_button = Button(self.bg_panel, image=pisces_photo, command=self.pisces, borderwidth=0)
        pisces_button.place(x=380, y=310)

        aves_image = Image.open("aves.png")
        aves_photo = ImageTk.PhotoImage(aves_image)
        img_aves = Label(image=aves_photo)
        img_aves.image = aves_photo
        aves_button = Button(self.bg_panel, image=aves_photo, command=self.aves, borderwidth=0)
        aves_button.place(x=640, y=290)

        reptil_image = Image.open("reptil.png")
        reptil_photo = ImageTk.PhotoImage(reptil_image)
        img_reptil = Label(image=reptil_photo)
        img_reptil.image = reptil_photo
        reptil_button = Button(self.bg_panel, image=reptil_photo, command=self.reptil, borderwidth=0)
        reptil_button.place(x=900, y=310)

    def read_csv(self, filename):
        data = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data

    def search(self):
        query = self.search_entry.get().lower()
        data = self.read_csv('List Hewan.csv')

        # Mengosongkan Listbox sebelum pencarian baru
        self.result_listbox.delete(0, 'end')

        # Implementasi pencarian sentinel linear
        found = False
        for index, row in enumerate(data):
            if query in row[0].lower():  # Misalnya, indeks 0 adalah kolom nama satwa
                found = True
                self.result_listbox.insert('end', row[0])  # Menambahkan hasil pencarian ke dalam listbox

        if not found:
            self.result_listbox.insert('end', 'Not found')

        # Mengikat fungsi callback untuk menampilkan informasi hewan saat diklik
        self.result_listbox.bind('<<ListboxSelect>>', self.show_animal_info)


    def show_animal_info(self, event):
    # Mendapatkan item yang dipilih dari listbox
        selected_item_index = self.result_listbox.curselection()
        if selected_item_index:
            selected_index = selected_item_index[0]
            selected_animal = self.result_listbox.get(selected_index)

            # Menampilkan informasi hewan berdasarkan nama yang dipilih
            info_mapping = {
                'Burung Merak (Pavo muticus)': 'info burung merak.png',
                'Burung Unta (Struthio camelus)': 'info burung unta.png',
                'Elang Bondol (Haliastur indus)': 'info elang bondol.png',
                'Burung Julang Emas (Aquila Chrysaetos)': 'info julang emas.png',
                'Burung Jalak Bali (Leucopsar Rothschildi)': 'info jalak bali.png',
                'Kakatua Jambul Kuning (Cacatua galerita)': 'info kakatua jambul kuning.png',
                'Burung Kakatua (Cacatuidae)': 'info kakatua.png',
                'Burung Merpati (Columba livia)': 'info merpati.png',
                'Nuri Bayan (Eclectus roratus)': 'info nuri bayan.png',
                'Pelikan (Pelecanus conspicillatus)': 'info pelikan.png',
                'Angsa Nila (Cygnus olor)': 'info angsa nila.png',
                'Burung Bangau Hitam (Egretta ardesiaca)': 'info bangau hitam.png',
                'Burung Camar (Larus argentatus)': 'info burung camar.png',
                'Burung Hantu (Strigiformes)': 'info burung hantu.png',
                'Cendrawasih (Paradisaeidae)': 'info cendrawasih.png',
                'Flamingo (Phoenicopterus ruber)': 'info flamingo.png',
                'Penguin Raja (Aptenodytes patagonicus)': 'info penguin.png',
                'Puffin Atlantik (Fratercula arctica)': 'info puffin atlantik',

                'Anoa (Bubalus spp.)': 'info anoa.png',
                'Babi Rusa (Babyrousa spp.)': 'info babi rusa.png',
                'Banteng (Bos Sondaicus)': 'info banteng.png',
                'Bekantan (Nasalis Larvatus)': 'info bekantan.png',
                'Harimau (Panthera tigris)': 'info harimau.png',
                'Koala (Phascolarctos cinereus)': 'info koala.png',
                'Orang utan (Pongo spp.)': 'info orang utan.png',
                'Panda Merah (Ailurus fulgens)': 'info panda merah.png',
                'Singa (Panthera leo)': 'info singa.png',
                'Zebra (Equus zebra)': 'info zebra.png',
                'Cheetah (Acinonyx jubatus)': 'info cheetah.png',
                'Beruang (Ursus arctos horribilis)': 'info beruang.png',
                'Unta (Camelus bactrianus)': 'info unta.png',
                'Kangguru (Macropodidae)': 'info kangguru.png',
                'Kuda Nil (Hippopotamus amphibius)': 'info kuda nil.png',
                'Gajah Asia (Elephas maximus)': 'info gajah asia.png',
                'Badak Sumatera (Dicerorhinus sumatrensis)': 'info badak sumatera.png',
                'Serigala (Canis lupus)': 'info serigala.png',

                'Ikan Arapaima (Arapaima gigas)': 'info ikan arapaima.png',
                'Ikan Arwana (Osteoglossum bicirrhosum)': 'info ikan arwana.png',
                'Ikan Buntal (Tetraodontidae)': 'info ikan buntal.png',
                'Ikan Gurame (Osphronemus goramy)': 'info ikan gurame.png',
                'Ikan Hiu (Selachimorpha)': 'info ikan hiu.png',
                'Ikan Koi (Cyprinus carpio)': 'info ikan koi.png',
                'Ikan Nila (Oreochromis niloticus)': 'info ikan nila.png',
                'Ikan Lele (Clarias gariepinus)': 'info ikan lele.png',
                'Ikan Kakap Merah (Lutjanus sebae)': 'info ikan kakap.png',
                'Ikan Piranha (Pygocentrus nattereri)': 'info ikan piranha.png',
                'Ikan Mackerel (Scombridae spp.)': 'info ikan mackerel.png',
                'Ikan Pike (Esox lucius)': 'info ikan pike.png',
                'Ikan Sardine (Sardinops sagax)': 'info ikan sardine.png',
                'Ikan Salmon (Salmo salar)': 'info ikan salmon.png',
                'Ikan Tuna (Thunnini)': 'info ikan tuna.png',
                'Ikan Pari (Dasyatidae)': 'info ikan pari.png',
                'Ikan Tenggiri (Scomberomorus commerson)': 'info ikan tenggiri.png',
                'Belut (Anguila spp.)': 'info belut.png',

                'Bunglon Daun (Brookesia micra)': 'info bunglon daun.png',
                'Bunglon (Chamaeleonidae)': 'info bunglon.png',
                'Kadal Tuatara (Sphenodon punctatus)': 'info tuatara.png',
                'Kadal Air (Varanus salvator)': 'info kadal air.png',
                'Kadal Komodo (Varanus komodoensis)': 'info komodo.png',
                'Kadal Balisisk (Basiliscus basiliscus)': 'info kadal basilisk.png',
                'Kadal Berduri (Moloch Horridus)': 'info kadal berduri.png',
                'Katak (Anura)': 'info katak.png',
                'Salamander (Caudata)': 'info salamander.png',
                'Tokek (Gecko gecko)': 'info tokek.png',
                'Ular Bertanduk (Pseudocerastes Urarachnoides)': 'info ular bertanduk.png',
                'Anakonda (Eunectes)': 'info anakonda.png',
                'Biawak Hijau (Varanus prasinus)': 'info biawak.png',
                'Buaya Irian (Crocodylus novaeguineae)': 'info buaya.png',
                'Iguana (Iguanidae)': 'info iguana.png',
                'Ular Kobra Jawa (Naja sputatrix)': 'info kobra.png',
                'Kura-Kura (Testudinidae)': 'info kura-kura.png',
                'Penyu (Testudines)': 'info penyu.png'
            }
            if selected_animal in info_mapping:
                info_image_path = info_mapping[selected_animal]
                self.show_hewan_info(info_image_path)

    def show_hewan_info(self, info_image_path):

        # Membuka gambar dan membuat PhotoImage
        info_image = Image.open(info_image_path)
        image_width, image_height = info_image.size
        info_photo = ImageTk.PhotoImage(info_image)

        window_width = max(image_width, 800)
        window_height = max (image_height, 500)

        # Membuka jendela baru untuk menampilkan informasi hewan
        info_window = Toplevel()
        info_window.geometry(f'{window_width}x{window_height}')
        info_window.title('Informasi Hewan')

        # Membuat frame utama
        main_frame = Frame(info_window)
        main_frame.pack(fill=BOTH, expand=YES)

        # Membuat canvas dengan scrollbar
        canvas = Canvas(main_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        # Membuat frame untuk menampung gambar/info hewan
        bg_panel = Frame(canvas)
        canvas.create_window((0, 0), window=bg_panel, anchor="nw")

        # Menampilkan gambar dengan Label
        info_label = Label(bg_panel, image=info_photo)
        info_label.image = info_photo  # Simpan referensi ke objek PhotoImage agar tidak dihapus
        info_label.pack(fill='both', expand='yes')

    #=== MAMALIA ===#
    def mamalia(self):
        peraturan_bg = Toplevel()
        peraturan_bg.geometry('1270x700')
        peraturan_bg.state('zoomed')
        peraturan_bg.title('Satwa')

        # Create a frame to contain all widgets
        main_frame = Frame(peraturan_bg)
        main_frame.pack(fill=BOTH, expand=YES)

        # Create canvas with scrollbar
        canvas = Canvas(main_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.config(yscrollcommand=scrollbar.set)

        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame to contain your images/buttons
        bg_panel = Frame(canvas)
        canvas.create_window((0, 0), window=bg_panel, anchor="nw")

        # Background
        photo_frame = Image.open("bg frame.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        bg_label = Label(bg_panel, image=photo_bg)
        bg_label.image = photo_bg
        bg_label.pack(fill='both', expand='yes')

        # Add side image
        side_image = Image.open("teks m.png")
        side_photo = ImageTk.PhotoImage(side_image)
        side_label = Label(bg_panel, image=side_photo)
        side_label.image = side_photo
        side_label.place(x=0, y=10)

        # Informasi Mamalia
        info_anoa = ImageTk.PhotoImage(Image.open("info anoa.png"))
        info_babi_rusa = ImageTk.PhotoImage(Image.open("info babi rusa.png"))
        info_banteng = ImageTk.PhotoImage(Image.open("info banteng.png"))
        info_bekantan = ImageTk.PhotoImage(Image.open("info bekantan.png"))
        info_harimau = ImageTk.PhotoImage(Image.open("info harimau.png"))
        info_koala = ImageTk.PhotoImage(Image.open("info koala.png"))
        info_orang_utan = ImageTk.PhotoImage(Image.open("info orang utan.png"))
        info_panda_merah = ImageTk.PhotoImage(Image.open("info panda merah.png"))
        info_singa = ImageTk.PhotoImage(Image.open("info singa.png"))
        info_zebra = ImageTk.PhotoImage(Image.open("info zebra.png"))

        info_cheetah = ImageTk.PhotoImage(Image.open("info cheetah.png"))
        info_beruang = ImageTk.PhotoImage(Image.open("info beruang.png"))
        info_unta = ImageTk.PhotoImage(Image.open("info unta.png"))
        info_kangguru = ImageTk.PhotoImage(Image.open("info kangguru.png"))
        info_kuda_nil = ImageTk.PhotoImage(Image.open("info kuda nil.png"))
        info_gajah_asia = ImageTk.PhotoImage(Image.open("info gajah asia.png"))
        info_badak_sumatera = ImageTk.PhotoImage(Image.open("info badak sumatera.png"))
        info_serigala = ImageTk.PhotoImage(Image.open("info serigala.png"))


        satwa_image = Image.open("anoa.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_anoa), borderwidth=0)
        satwa_button.place(x=200, y=150)

        satwa_image = Image.open("babi rusa.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_babi_rusa), borderwidth=0)
        satwa_button.place(x=700, y=150)

        satwa_image = Image.open("banteng.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_banteng), borderwidth=0)
        satwa_button.place(x=200, y=400)

        satwa_image = Image.open("bekantan.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_bekantan), borderwidth=0)
        satwa_button.place(x=700, y=400)

        satwa_image = Image.open("harimau.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_harimau), borderwidth=0)
        satwa_button.place(x=200, y=650)

        satwa_image = Image.open("koala.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_koala), borderwidth=0)
        satwa_button.place(x=700, y=650)

        satwa_image = Image.open("orang utan.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_orang_utan), borderwidth=0)
        satwa_button.place(x=200, y=900)

        satwa_image = Image.open("panda merah.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_panda_merah), borderwidth=0)
        satwa_button.place(x=700, y=900)

        satwa_image = Image.open("singa.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_singa), borderwidth=0)
        satwa_button.place(x=200, y=1150)

        satwa_image = Image.open("zebra.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_zebra), borderwidth=0)
        satwa_button.place(x=700, y=1150)

        satwa_image = Image.open("cheetah.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_cheetah), borderwidth=0)
        satwa_button.place(x=200, y=1400)

        satwa_image = Image.open("beruang.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_beruang), borderwidth=0)
        satwa_button.place(x=700, y=1400)

        satwa_image = Image.open("unta.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_unta), borderwidth=0)
        satwa_button.place(x=200, y=1650)

        satwa_image = Image.open("kangguru.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_kangguru), borderwidth=0)
        satwa_button.place(x=700, y=1650)

        satwa_image = Image.open("kuda nil.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_kuda_nil), borderwidth=0)
        satwa_button.place(x=200, y=1900)

        satwa_image = Image.open("gajah asia.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_gajah_asia), borderwidth=0)
        satwa_button.place(x=700, y=1900)

        satwa_image = Image.open("badak sumatera.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_badak_sumatera), borderwidth=0)
        satwa_button.place(x=200, y=2150)

        satwa_image = Image.open("serigala.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_mamalia_info(info_serigala), borderwidth=0)
        satwa_button.place(x=700, y=2150)


    def show_mamalia_info(self, mamalia_info_image):
        image_window = Toplevel(self.peraturan_bg)
        image_window.title("Informasi Hewan Mamalia")

        label = Label(image_window, image=mamalia_info_image)
        label.image = mamalia_info_image
        label.pack()

        # Memanggil metode untuk mendapatkan ukuran dan posisi jendela
        x, y = self.get_window_position(image_window)

        # Mengatur geometri jendela Toplevel
        image_window.geometry(f"+{x}+{y}")


    #=== PISCES ===#
    def pisces(self):
        peraturan_bg = Toplevel()
        peraturan_bg.geometry('1270x700')
        peraturan_bg.state('zoomed')
        peraturan_bg.title('Satwa')

       # Create a frame to contain all widgets
        main_frame = Frame(peraturan_bg)
        main_frame.pack(fill=BOTH, expand=YES)

        # Create canvas with scrollbar
        canvas = Canvas(main_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.config(yscrollcommand=scrollbar.set)

        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame to contain your images/buttons
        bg_panel = Frame(canvas)
        canvas.create_window((0, 0), window=bg_panel, anchor="nw")

        # Background
        photo_frame = Image.open("bg frame.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        bg_label = Label(bg_panel, image=photo_bg)
        bg_label.image = photo_bg
        bg_label.pack(fill='both', expand='yes')

        # Add side image
        side_image = Image.open("teks p.png")
        side_photo = ImageTk.PhotoImage(side_image)
        side_label = Label(bg_panel, image=side_photo)
        side_label.image = side_photo
        side_label.place(x=0, y=10)

        # Informasi Pisces
        info_ikan_arapaima = ImageTk.PhotoImage(Image.open("info ikan arapaima.png"))
        info_ikan_piranha = ImageTk.PhotoImage(Image.open("info ikan piranha.png"))
        info_ikan_arwana = ImageTk.PhotoImage(Image.open("info ikan arwana.png"))
        info_ikan_koi = ImageTk.PhotoImage(Image.open("info ikan koi.png"))
        info_ikan_tuna = ImageTk.PhotoImage(Image.open("info ikan tuna.png"))
        info_ikan_lele = ImageTk.PhotoImage(Image.open("info ikan lele.png"))
        info_ikan_gurame = ImageTk.PhotoImage(Image.open("info ikan gurame.png"))
        info_ikan_pari = ImageTk.PhotoImage(Image.open("info ikan pari.png"))
        info_ikan_buntal = ImageTk.PhotoImage(Image.open("info ikan buntal.png"))
        info_ikan_hiu = ImageTk.PhotoImage(Image.open("info ikan hiu.png"))
        info_belut = ImageTk.PhotoImage(Image.open("info belut.png"))
        info_ikan_kakap = ImageTk.PhotoImage(Image.open("info ikan kakap.png"))
        info_ikan_nila = ImageTk.PhotoImage(Image.open("info ikan nila.png"))
        info_ikan_salmon = ImageTk.PhotoImage(Image.open("info ikan salmon.png"))
        info_ikan_sardine = ImageTk.PhotoImage(Image.open("info ikan sardine.png"))
        info_ikan_pike = ImageTk.PhotoImage(Image.open("info ikan pike.png"))
        info_ikan_tenggiri = ImageTk.PhotoImage(Image.open("info ikan tenggiri.png"))
        info_ikan_mackerel = ImageTk.PhotoImage(Image.open("info ikan mackerel.png"))


        satwa_image = Image.open("ikan arapaima.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_arapaima), borderwidth=0)
        satwa_button.place(x=200, y=150)

        satwa_image = Image.open("ikan piranha.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_piranha), borderwidth=0)
        satwa_button.place(x=700, y=150)

        satwa_image = Image.open("ikan arwana.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_arwana), borderwidth=0)
        satwa_button.place(x=200, y=400)

        satwa_image = Image.open("ikan koi.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_koi), borderwidth=0)
        satwa_button.place(x=700, y=400)

        satwa_image = Image.open("ikan tuna.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_tuna), borderwidth=0)
        satwa_button.place(x=200, y=650)

        satwa_image = Image.open("ikan lele.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_lele), borderwidth=0)
        satwa_button.place(x=700, y=650)

        satwa_image = Image.open("ikan gurame.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_gurame), borderwidth=0)
        satwa_button.place(x=200, y=900)

        satwa_image = Image.open("ikan pari.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_pari), borderwidth=0)
        satwa_button.place(x=700, y=900)

        satwa_image = Image.open("ikan buntal.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_buntal), borderwidth=0)
        satwa_button.place(x=200, y=1150)

        satwa_image = Image.open("ikan hiu.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_hiu), borderwidth=0)
        satwa_button.place(x=700, y=1150)

        satwa_image = Image.open("belut.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_belut), borderwidth=0)
        satwa_button.place(x=200, y=1400)

        satwa_image = Image.open("ikan kakap.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_kakap), borderwidth=0)
        satwa_button.place(x=700, y=1400)

        satwa_image = Image.open("ikan nila.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_nila), borderwidth=0)
        satwa_button.place(x=200, y=1650)

        satwa_image = Image.open("ikan salmon.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_salmon), borderwidth=0)
        satwa_button.place(x=700, y=1650)

        satwa_image = Image.open("ikan sardine.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_sardine), borderwidth=0)
        satwa_button.place(x=200, y=1900)

        satwa_image = Image.open("ikan pike.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_pike), borderwidth=0)
        satwa_button.place(x=700, y=1900)

        satwa_image = Image.open("ikan tenggiri.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_tenggiri), borderwidth=0)
        satwa_button.place(x=200, y=2150)

        satwa_image = Image.open("ikan mackerel.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_pisces_info(info_ikan_mackerel), borderwidth=0)
        satwa_button.place(x=700, y=2150)

    def show_pisces_info(self, pisces_info_image):
        image_window = Toplevel(self.peraturan_bg)
        image_window.title("Informasi Hewan Pisces")

        label = Label(image_window, image=pisces_info_image)
        label.image = pisces_info_image
        label.pack()

        # Memanggil metode untuk mendapatkan ukuran dan posisi jendela
        x, y = self.get_window_position(image_window)

        # Mengatur geometri jendela Toplevel
        image_window.geometry(f"+{x}+{y}")


    #=== AVES ===#
    def aves(self):
        peraturan_bg = Toplevel()
        peraturan_bg.geometry('1270x1300')
        peraturan_bg.state('zoomed')
        peraturan_bg.title('Satwa')

        # Create a frame to contain all widgets
        main_frame = Frame(peraturan_bg)
        main_frame.pack(fill=BOTH, expand=YES)

        # Create canvas with scrollbar
        canvas = Canvas(main_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.config(yscrollcommand=scrollbar.set)

        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame to contain your images/buttons
        bg_panel = Frame(canvas)
        canvas.create_window((0, 0), window=bg_panel, anchor="nw")

        # Add background image
        photo_frame = Image.open("bg frame.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        bg_label = Label(bg_panel, image=photo_bg)
        bg_label.image = photo_bg
        bg_label.pack(fill='both', expand='yes')

        # Add side image
        side_image = Image.open("teks a.png")
        side_photo = ImageTk.PhotoImage(side_image)
        side_label = Label(bg_panel, image=side_photo)
        side_label.image = side_photo
        side_label.place(x=0, y=10)

        # Informasi Aves
        info_elang_bondol = ImageTk.PhotoImage(Image.open("info elang bondol.png"))
        info_jalak_bali = ImageTk.PhotoImage(Image.open("info jalak bali.png"))
        info_julang_emas = ImageTk.PhotoImage(Image.open("info julang emas.png"))
        info_kakatua_jambul_kuning = ImageTk.PhotoImage(Image.open("info kakatua jambul kuning.png"))
        info_pelikan = ImageTk.PhotoImage(Image.open("info pelikan.png"))
        info_nuri_bayan = ImageTk.PhotoImage(Image.open("info nuri bayan.png"))
        info_burung_unta = ImageTk.PhotoImage(Image.open("info burung unta.png"))
        info_burung_merak = ImageTk.PhotoImage(Image.open("info burung merak.png"))
        info_merpati = ImageTk.PhotoImage(Image.open("info merpati.png"))
        info_kakatua = ImageTk.PhotoImage(Image.open("info kakatua.png"))
        info_burung_hantu = ImageTk.PhotoImage(Image.open("info burung hantu.png"))
        info_penguin = ImageTk.PhotoImage(Image.open("info penguin.png"))
        info_flamingo = ImageTk.PhotoImage(Image.open("info flamingo.png"))
        info_bangau_hitam = ImageTk.PhotoImage(Image.open("info bangau hitam.png"))
        info_burung_camar = ImageTk.PhotoImage(Image.open("info burung camar.png"))
        info_angsa_nila = ImageTk.PhotoImage(Image.open("info angsa nila.png"))
        info_cendrawasih = ImageTk.PhotoImage(Image.open("info cendrawasih.png"))
        info_puffin_atlantik = ImageTk.PhotoImage(Image.open("info puffin atlantik.png"))

        satwa_image = Image.open("elang bondol.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_elang_bondol), borderwidth=0)
        satwa_button.place(x=200, y=150)

        satwa_image = Image.open("jalak bali.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_jalak_bali), borderwidth=0)
        satwa_button.place(x=700, y=150)

        satwa_image = Image.open("julang emas.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_julang_emas), borderwidth=0)
        satwa_button.place(x=200, y=400)

        satwa_image = Image.open("kakatua jambul kuning.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_kakatua_jambul_kuning), borderwidth=0)
        satwa_button.place(x=700, y=400)

        satwa_image = Image.open("pelikan.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_pelikan), borderwidth=0)
        satwa_button.place(x=200, y=650)

        satwa_image = Image.open("nuri bayan.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_nuri_bayan), borderwidth=0)
        satwa_button.place(x=700, y=650)

        satwa_image = Image.open("burung unta.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_burung_unta), borderwidth=0)
        satwa_button.place(x=200, y=900)

        satwa_image = Image.open("burung merak.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_burung_merak), borderwidth=0)
        satwa_button.place(x=700, y=900)

        satwa_image = Image.open("merpati.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_merpati), borderwidth=0)
        satwa_button.place(x=200, y=1150)

        satwa_image = Image.open("kakatua.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_kakatua), borderwidth=0)
        satwa_button.place(x=700, y=1150)

        satwa_image = Image.open("burung hantu.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_burung_hantu), borderwidth=0)
        satwa_button.place(x=200, y=1400)

        satwa_image = Image.open("penguin.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_penguin), borderwidth=0)
        satwa_button.place(x=700, y=1400)

        satwa_image = Image.open("flamingo.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_flamingo), borderwidth=0)
        satwa_button.place(x=200, y=1650)

        satwa_image = Image.open("bangau hitam.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_bangau_hitam), borderwidth=0)
        satwa_button.place(x=700, y=1650)

        satwa_image = Image.open("burung camar.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_burung_camar), borderwidth=0)
        satwa_button.place(x=200, y=1900)

        satwa_image = Image.open("angsa nila.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_angsa_nila), borderwidth=0)
        satwa_button.place(x=700, y=1900)

        satwa_image = Image.open("cendrawasih.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_cendrawasih), borderwidth=0)
        satwa_button.place(x=200, y=2150)

        satwa_image = Image.open("puffin atlantik.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_aves_info(info_puffin_atlantik), borderwidth=0)
        satwa_button.place(x=700, y=2150)

    def show_aves_info(self, aves_info_image):
        image_window = Toplevel(self.peraturan_bg)
        image_window.title("Informasi Hewan Aves")

        label = Label(image_window, image=aves_info_image)
        label.image = aves_info_image
        label.pack()

        # Memanggil metode untuk mendapatkan ukuran dan posisi jendela
        x, y = self.get_window_position(image_window)

        # Mengatur geometri jendela Toplevel
        image_window.geometry(f"+{x}+{y}")


    #=== REPTIL ===#
    def reptil(self):
        peraturan_bg = Toplevel()
        peraturan_bg.geometry('1270x700')
        peraturan_bg.state('zoomed')
        peraturan_bg.title('Satwa')

        # Create a frame to contain all widgets
        main_frame = Frame(peraturan_bg)
        main_frame.pack(fill=BOTH, expand=YES)

        # Create canvas with scrollbar
        canvas = Canvas(main_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.config(yscrollcommand=scrollbar.set)

        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame to contain your images/buttons
        bg_panel = Frame(canvas)
        canvas.create_window((0, 0), window=bg_panel, anchor="nw")

        # Background
        photo_frame = Image.open("bg frame.png")
        photo_bg = ImageTk.PhotoImage(photo_frame)
        bg_label = Label(bg_panel, image=photo_bg)
        bg_label.image = photo_bg
        bg_label.pack(fill='both', expand='yes')

        # Side image
        side_image = Image.open("teks r.png")
        side_photo = ImageTk.PhotoImage(side_image)
        side_label = Label(bg_panel, image=side_photo)
        side_label.image = side_photo
        side_label.place(x=0, y=10)

        # Informasi Reptil
        info_anakonda = ImageTk.PhotoImage(Image.open("info anakonda.png"))
        info_biawak = ImageTk.PhotoImage(Image.open("info biawak.png"))
        info_buaya = ImageTk.PhotoImage(Image.open("info buaya.png"))
        info_bunglon = ImageTk.PhotoImage(Image.open("info bunglon.png"))
        info_iguana = ImageTk.PhotoImage(Image.open("info iguana.png"))
        info_kadal_air = ImageTk.PhotoImage(Image.open("info kadal air.png"))
        info_kobra = ImageTk.PhotoImage(Image.open("info kobra.png"))
        info_komodo = ImageTk.PhotoImage(Image.open("info komodo.png"))
        info_kura_kura = ImageTk.PhotoImage(Image.open("info kura-kura.png"))
        info_penyu = ImageTk.PhotoImage(Image.open("info penyu.png"))
        info_katak = ImageTk.PhotoImage(Image.open("info katak.png"))
        info_tokek = ImageTk.PhotoImage(Image.open("info tokek.png"))
        info_salamander = ImageTk.PhotoImage(Image.open("info salamander.png"))
        info_tuatara = ImageTk.PhotoImage(Image.open("info tuatara.png"))
        info_kadal_basilisk = ImageTk.PhotoImage(Image.open("info kadal basilisk.png"))
        info_kadal_berduri = ImageTk.PhotoImage(Image.open("info kadal berduri.png"))
        info_bunglon_daun = ImageTk.PhotoImage(Image.open("info bunglon daun.png"))
        info_ular_bertanduk = ImageTk.PhotoImage(Image.open("info ular bertanduk.png"))

        satwa_image = Image.open("anakonda.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_anakonda), borderwidth=0)
        satwa_button.place(x=200, y=165)

        satwa_image = Image.open("biawak.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_biawak), borderwidth=0)
        satwa_button.place(x=700, y=165)

        satwa_image = Image.open("buaya.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_buaya), borderwidth=0)
        satwa_button.place(x=200, y=400)

        satwa_image = Image.open("bunglon.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_bunglon), borderwidth=0)
        satwa_button.place(x=700, y=400)

        satwa_image = Image.open("iguana.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_iguana), borderwidth=0)
        satwa_button.place(x=200, y=650)

        satwa_image = Image.open("kadal air.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_kadal_air), borderwidth=0)
        satwa_button.place(x=700, y=650)

        satwa_image = Image.open("kobra.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_kobra), borderwidth=0)
        satwa_button.place(x=200, y=900)

        satwa_image = Image.open("komodo.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_komodo), borderwidth=0)
        satwa_button.place(x=700, y=900)

        satwa_image = Image.open("kura-kura.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_kura_kura), borderwidth=0)
        satwa_button.place(x=200, y=1150)

        satwa_image = Image.open("penyu.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_penyu), borderwidth=0)
        satwa_button.place(x=700, y=1150)

        satwa_image = Image.open("katak.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_katak), borderwidth=0)
        satwa_button.place(x=200, y=1400)

        satwa_image = Image.open("tokek.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_tokek), borderwidth=0)
        satwa_button.place(x=700, y=1400)

        satwa_image = Image.open("salamander.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_salamander), borderwidth=0)
        satwa_button.place(x=200, y=1650)

        satwa_image = Image.open("tuatara.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_tuatara), borderwidth=0)
        satwa_button.place(x=700, y=1650)

        satwa_image = Image.open("kadal basilisk.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_kadal_basilisk), borderwidth=0)
        satwa_button.place(x=200, y=1900)

        satwa_image = Image.open("kadal berduri.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_kadal_berduri), borderwidth=0)
        satwa_button.place(x=700, y=1900)

        satwa_image = Image.open("bunglon daun.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_bunglon_daun), borderwidth=0)
        satwa_button.place(x=200, y=2150)

        satwa_image = Image.open("ular bertanduk.png")
        satwa_photo = ImageTk.PhotoImage(satwa_image)
        img_satwa = Label(image=satwa_photo)
        img_satwa.image = satwa_photo
        satwa_button = Button(bg_panel, image=satwa_photo, command=lambda: self.show_reptil_info(info_ular_bertanduk), borderwidth=0)
        satwa_button.place(x=700, y=2150)

    def show_reptil_info(self, reptil_info_image):
        image_window = Toplevel(self.peraturan_bg)
        image_window.title("Informasi Hewan Reptil")

        label = Label(image_window, image=reptil_info_image)
        label.image = reptil_info_image
        label.pack()

        # Memanggil metode untuk mendapatkan ukuran dan posisi jendela
        x, y = self.get_window_position(image_window)

        # Mengatur geometri jendela Toplevel
        image_window.geometry(f"+{x}+{y}")


    def get_window_position(self, window):
        # Mendapatkan ukuran layar
        screen_width = self.peraturan_bg.winfo_screenwidth()
        screen_height = self.peraturan_bg.winfo_screenheight()

        # Mendapatkan ukuran jendela
        window.update_idletasks()  # Memperbarui ukuran jendela
        window_width = window.winfo_reqwidth()
        window_height = window.winfo_reqheight()

        # Menghitung posisi x dan y untuk menempatkan jendela
        x = (screen_width // 3) - (window_width // 3)
        y = (screen_height // 3) - (window_height // 3)

        return x, y


if __name__ == "__main__":
    root = Tk()
    app = ZooTopia(root)
    root.mainloop()
