import tkinter as tk
from tkinter import messagebox
from controllers.book_controller import fetch_books
from PIL import Image, ImageTk, ImageDraw
import os
import threading
import time

class MemberDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Katalog Buku - Perpustakaan Digital")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f5f5f5")

        self.images = []
        self.all_books = fetch_books()

        # ================= STATE PINJAMAN =================
        self.borrowed_books = []
        
        # ================= AUTO REFRESH =================
        self.is_running = True
        self.last_book_count = len(self.all_books)
        self.start_auto_refresh()

        # ================= HEADER =================
        header = tk.Frame(root, bg="#0078d4", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # LEFT LOGO
        left = tk.Frame(header, bg="#0078d4")
        left.pack(side="left", padx=30, pady=15)

        tk.Label(left, text="📚", bg="#0078d4", font=("Segoe UI", 28)).pack(side="left")
        tk.Label(
            left, text="Perpustakaan Digital",
            bg="#0078d4", fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(side="left", padx=12)

        # CENTER SEARCH
        center = tk.Frame(header, bg="#0078d4")
        center.pack(side="left", expand=True, padx=30)

        search_frame = tk.Frame(center, bg="white")
        search_frame.pack(fill="x", expand=True)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 12),
            border=0
        )
        search_entry.pack(side="left", padx=15, pady=12, fill="x", expand=True)
        search_entry.bind("<KeyRelease>", self.search_books)

        tk.Button(
            search_frame,
            text="🔍",
            relief="flat",
            bg="white",
            border=0,
            command=self.search_books
        ).pack(side="right", padx=10)

        # RIGHT MENU
        right = tk.Frame(header, bg="#0078d4")
        right.pack(side="right", padx=30)

        tk.Button(
            right,
            text="� Refresh",
            bg="white",
            fg="#0078d4",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            command=self.refresh_books
        ).pack(side="left", padx=10)

        tk.Button(
            right,
            text="👤 Logout",
            bg="white",
            fg="#0078d4",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            command=self.logout
        ).pack(side="left", padx=10)

        tk.Button(
            right,
            text="🛒 Paket",
            bg="#ffc107",
            fg="black",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            command=self.open_paket
        ).pack(side="left")

        # ================= CONTENT =================
        body = tk.Frame(root, bg="#f5f5f5")
        body.pack(fill="both", expand=True, padx=30, pady=20)

        # Status bar
        status_frame = tk.Frame(body, bg="#e8f5e9", height=30)
        status_frame.pack(fill="x", pady=(0, 15))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="🔄 Sinkronisasi otomatis aktif",
            bg="#e8f5e9",
            fg="#27ae60",
            font=("Segoe UI", 9)
        )
        self.status_label.pack(anchor="w", padx=15, pady=7)

        tk.Label(
            body,
            text="Buku-Baru",
            bg="#f5f5f5",
            font=("Segoe UI", 18, "bold"),
            fg="#333"
        ).pack(anchor="w", pady=(0, 20))

        canvas = tk.Canvas(body, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(body, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.outer_frame = tk.Frame(canvas, bg="#f5f5f5")
        canvas.create_window((0, 0), window=self.outer_frame, anchor="nw")

        self.outer_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.grid_frame = tk.Frame(self.outer_frame, bg="#f5f5f5")
        self.grid_frame.pack(anchor="nw")

        self.render_books(self.all_books)

        # ================= FOOTER =================
        footer = tk.Frame(root, bg="#333", height=50)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="© 2025 Perpus.org - All rights reserved. Email: perpus.org@gmail.com",
            bg="#333",
            fg="white",
            font=("Segoe UI", 9)
        ).pack(pady=12)

    # ================= RENDER =================
    def render_books(self, books):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        CARD_W = 180
        GAP = 20
        MAX_WIDTH = 1200
        max_col = max(1, MAX_WIDTH // (CARD_W + GAP))

        row = col = 0
        for book in books:
            self.book_card(book, row, col)
            col += 1
            if col >= max_col:
                col = 0
                row += 1

    # ================= SEARCH =================
    def search_books(self, event=None):
        q = self.search_var.get().lower()
        if not q:
            self.render_books(self.all_books)
            return

        filtered = [
            b for b in self.all_books
            if q in b[1].lower() or q in b[2].lower()
        ]
        self.render_books(filtered)

    # ================= LOGOUT =================
    def logout(self):
        if messagebox.askyesno("Logout", "Yakin ingin keluar?"):
            self.is_running = False  # Stop auto-refresh thread
            try:
                # Import here to avoid circular imports at module load
                from views.login_view import LoginView
                self.root.destroy()

                # Open a fresh root and show login view
                root = tk.Tk()
                LoginView(root)
                root.mainloop()
            except Exception:
                # Fallback: just destroy root if anything goes wrong
                try:
                    self.root.destroy()
                except:
                    pass

    # ================= REFRESH BOOKS =================
    def refresh_books(self):
        """Refresh daftar buku dari database"""
        self.all_books = fetch_books()
        self.search_var.set("")
        self.render_books(self.all_books)
        messagebox.showinfo("Sukses", "Daftar buku telah diperbarui!")

    # ================= AUTO REFRESH =================
    def start_auto_refresh(self):
        """Start background thread untuk auto-refresh database changes"""
        thread = threading.Thread(target=self.auto_refresh_worker, daemon=True)
        thread.daemon = True
        thread.start()
    
    def auto_refresh_worker(self):
        """Worker thread untuk check perubahan database setiap 5 detik"""
        while self.is_running:
            try:
                time.sleep(5)  # Check setiap 5 detik
                
                # Cek apakah ada buku baru
                current_books = fetch_books()
                current_count = len(current_books)
                
                if current_count > self.last_book_count:
                    # Ada buku baru ditambahkan
                    new_count = current_count - self.last_book_count
                    self.last_book_count = current_count
                    self.all_books = current_books
                    
                    # Update UI di main thread
                    self.root.after(0, lambda n=new_count: self.show_refresh_notification(f"Ada {n} buku baru!"))
                    self.root.after(0, self.update_display)
                    
                elif current_count < self.last_book_count:
                    # Ada buku yang dihapus
                    self.last_book_count = current_count
                    self.all_books = current_books
                    self.root.after(0, self.update_display)
                    
            except Exception as e:
                pass  # Silent fail, jangan interrupt user
    
    def show_refresh_notification(self, message):
        """Tampilkan notifikasi perubahan data"""
        try:
            # Update status bar
            self.status_label.config(text=f"✓ {message}")
            
            # Auto revert status setelah 5 detik
            self.root.after(5000, lambda: self.status_label.config(text="🔄 Sinkronisasi otomatis aktif"))
            
        except:
            pass
    
    def update_display(self):
        """Update tampilan buku (dipanggil dari auto-refresh)"""
        try:
            current_search = self.search_var.get().lower()
            if current_search:
                # Jika ada search, filter hasil baru
                filtered = [
                    b for b in self.all_books
                    if current_search in b[1].lower() or current_search in b[2].lower()
                ]
                self.render_books(filtered)
            else:
                # Tampilkan semua buku
                self.render_books(self.all_books)
        except:
            pass

    # ================= PINJAM =================
    def pinjam_buku(self, book, popup):
        if book[3] <= 0:  # Check stok
            messagebox.showerror("Gagal", f"Stok buku '{book[1]}' tidak tersedia.")
            return
        
        if any(b[0] == book[0] for b in self.borrowed_books):  # Check already borrowed
            messagebox.showwarning("Peringatan", f"Anda sudah meminjam buku '{book[1]}'.")
            return

        self.borrowed_books.append(book)
        messagebox.showinfo("Berhasil", f"Buku '{book[1]}' berhasil dipinjam.\n\nTanggal kembali: 7 hari")
        popup.destroy()

    def hapus_buku_pinjam(self, book, popup):
        """Hapus buku dari daftar pinjaman"""
        if messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus '{book[1]}' dari pinjaman?"):
            self.borrowed_books.remove(book)
            messagebox.showinfo("Berhasil", f"Buku '{book[1]}' telah dihapus dari pinjaman.")
            popup.destroy()
            self.open_paket()

    # ================= PAKET =================
    def rounded_image(self, img, radius=8):
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius, fill=255)
        img.putalpha(mask)
        return img

    def book_card(self, book, row, col):
        frame = tk.Frame(self.grid_frame, bg="white", cursor="hand2")
        frame.grid(row=row, column=col, padx=10, pady=15)

        path = book[4] if book[4] and os.path.exists(book[4]) else None
        if path:
            img = Image.open(path).resize((160, 220))
        else:
            img = Image.new('RGBA', (160, 220), (240, 240, 240, 255))
        img = self.rounded_image(img)

        photo = ImageTk.PhotoImage(img)
        self.images.append(photo)

        tk.Label(frame, image=photo, bg="white").pack(padx=8, pady=8)
        tk.Label(frame, text=book[1], bg="white", font=("Segoe UI", 10, "bold"), wraplength=150).pack(anchor="w", padx=8)
        tk.Label(frame, text=f"Penulis: {book[2]}", bg="white", fg="#666", font=("Segoe UI", 8)).pack(anchor="w", padx=8)
        
        # Stok display
        stok_color = "#27ae60" if book[3] > 0 else "#e74c3c"
        stok_text = f"Stok: {book[3]} tersedia" if book[3] > 0 else "Stok: Tidak tersedia"
        tk.Label(frame, text=stok_text, bg="white", fg=stok_color, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=8, pady=(0, 8))

        frame.bind("<Button-1>", lambda e, b=book: self.open_detail(b))

    # ================= DETAIL =================
    def open_detail(self, book):
        popup = tk.Toplevel(self.root)
        popup.title("Detail Buku")
        popup.geometry("480x600")
        popup.configure(bg="white")
        popup.transient(self.root)
        popup.grab_set()

        path = book[4] if book[4] and os.path.exists(book[4]) else None
        if path:
            img = Image.open(path).resize((200, 280))
        else:
            img = Image.new('RGBA', (200, 280), (240, 240, 240, 255))
        img = self.rounded_image(img)

        photo = ImageTk.PhotoImage(img)
        self.images.append(photo)

        tk.Label(popup, image=photo, bg="white").pack(pady=15)
        tk.Label(popup, text=book[1], bg="white", font=("Segoe UI", 14, "bold")).pack()
        tk.Label(popup, text=f"Penulis: {book[2]}", bg="white").pack()
        tk.Label(popup, text=f"Penerbit: {book[6]}", bg="white").pack()
        tk.Label(popup, text=f"Tahun Terbit: {book[7]}", bg="white").pack()
        
        # Stok display
        stok_color = "#27ae60" if book[3] > 0 else "#e74c3c"
        stok_text = f"Stok tersedia: {book[3]} buku" if book[3] > 0 else "Stok: Tidak tersedia"
        tk.Label(popup, text=stok_text, bg="white", fg=stok_color, font=("Segoe UI", 11, "bold")).pack(pady=10)

        btn_state = "normal" if book[3] > 0 else "disabled"
        tk.Button(
            popup,
            text="📖 Pinjam Buku",
            bg="#0078d4" if book[3] > 0 else "#bdc3c7",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=30,
            pady=12,
            state=btn_state,
            command=lambda b=book, p=popup: self.pinjam_buku(b, p)
        ).pack(pady=20)

    # ================= PAKET =================
    def open_paket(self):
        popup = tk.Toplevel(self.root)
        popup.title("Paket Saya")
        popup.geometry("500x600")
        popup.configure(bg="white")
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(
            popup,
            text="📦 Buku yang Saya Pinjam",
            bg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=20)

        if not self.borrowed_books:
            tk.Label(
                popup,
                text="Belum ada buku yang dipinjam.",
                bg="white",
                fg="#666"
            ).pack(pady=40)
            return

        for book in self.borrowed_books:
            card = tk.Frame(popup, bg="#f5f5f5")
            card.pack(fill="x", padx=20, pady=8)

            title_frame = tk.Frame(card, bg="#f5f5f5")
            title_frame.pack(fill="x", padx=10, pady=4)
            
            tk.Label(title_frame, text=book[1], bg="#f5f5f5", font=("Segoe UI", 11, "bold")).pack(side="left", fill="x", expand=True)
            tk.Button(title_frame, text="🗑️ Hapus", bg="#d32f2f", fg="white", font=("Segoe UI", 9), padx=8, pady=2, command=lambda b=book, p=popup: self.hapus_buku_pinjam(b, p)).pack(side="right")
            
            tk.Label(card, text=f"Penulis: {book[2]}", bg="#f5f5f5", fg="#555", font=("Segoe UI", 9)).pack(anchor="w", padx=10, pady=(0, 6))
