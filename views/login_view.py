# views/login_view.py
import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import login_user
from views.admin_dashboard import AdminDashboard
from views.member_dashboard import MemberDashboard

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Perpustakaan Digital")
        self.root.geometry("1000x700")
        self.root.configure(bg="#ffffff")

        primary = "#0b86df"

        # ===== HEADER =====
        header = tk.Frame(root, bg="white", height=70)
        header.pack(fill="x")

        # left: logo
        left = tk.Frame(header, bg="white")
        left.pack(side="left", padx=20)
        tk.Label(left, text="📚", bg="white", font=("Segoe UI Emoji", 28)).pack(side="left")
        tk.Label(left, text="Perpustakaan", bg="white", fg="#333", font=("Segoe UI", 14, "bold")).pack(side="left", padx=(8,0))

        # (search and right-side header actions removed to match requested UI)

        # ===== LOGIN CARD =====
        card = tk.Frame(root, bg="white", padx=30, pady=20, bd=1, relief="groove")
        card.place(relx=0.5, rely=0.45, anchor="center")
        card.configure(width=520)

        # Title with tabs (visual only)
        tabs = tk.Frame(card, bg="white")
        tabs.pack(fill="x")
        login_tab = tk.Label(tabs, text="Login", bg=primary, fg="white", font=("Segoe UI", 12, "bold"), padx=20, pady=8)
        login_tab.pack(side="left")
        reg_tab = tk.Label(tabs, text="Daftar", bg="white", fg=primary, font=("Segoe UI", 10), padx=20, pady=8)
        reg_tab.pack(side="left")

        # Header
        tk.Label(card, text="Kamu belum login", bg="white", fg="#333", font=("Segoe UI", 14, "bold")).pack(pady=(12,8))

        # Email
        tk.Label(card, text="Email address", bg="white", fg="#333", anchor="w").pack(fill="x")
        self.username_entry = tk.Entry(card, width=40, font=("Segoe UI", 10), bd=1, relief="solid")
        self.username_entry.pack(pady=(4,12))
        self._add_placeholder(self.username_entry, "Email")

        # Password
        tk.Label(card, text="Password", bg="white", fg="#333", anchor="w").pack(fill="x")
        self.password_entry = tk.Entry(card, width=40, font=("Segoe UI", 10), bd=1, relief="solid")
        self.password_entry.pack(pady=(4,12))
        self._add_placeholder(self.password_entry, "Password", password=True)

        # small note
        tk.Label(card, text="Nikmati berbagai layanan perpus setelah login", bg="white", fg="#6b6f76", font=("Segoe UI", 9)).pack(pady=(4,8))

        # Login button
        tk.Button(card, text="LOGIN SEKARANG", bg=primary, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=self.login).pack(fill="x", pady=(6,8))

        # OR and Google button
        tk.Label(card, text="atau", bg="white", fg="#6b6f76", font=("Segoe UI", 10)).pack(pady=(6,6))
        google_btn = tk.Button(card, text="  G Login via Google", bg="white", fg=primary, bd=1, relief="solid", padx=8)
        google_btn.pack(fill="x")

        # ===== CATEGORIES FOOTER (visual) =====
        cats = tk.Frame(root, bg="white")
        cats.place(relx=0.02, rely=0.85)
        tk.Label(cats, text="Kategori", bg="white", fg="#333", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        sample = "Kewirausahaan Keuangan Teknologi SMP Sosial dan Psikologi SMA Seni dan Desain Sastra SD Sains Romansa"
        tags = tk.Label(cats, text=sample, bg="white", fg="#0b86df", font=("Segoe UI", 9), wraplength=960, justify="left")
        tags.pack(anchor="w")

        # footer small links
        footer = tk.Frame(root, bg="#f5f8fb")
        footer.pack(side="bottom", fill="x")
        links = tk.Label(footer, text="Privacy Policy   Terms Of Service   Donasi Buku   Request Buku", bg="#f5f8fb", fg="#0b86df", font=("Segoe UI", 9))
        links.pack(pady=8)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = login_user(username, password)

        if user:
            _, role = user
            self.root.destroy()
            root = tk.Tk()

            if role == "admin":
                AdminDashboard(root)
            else:
                MemberDashboard(root)

            root.mainloop()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah")

    def _add_placeholder(self, entry, placeholder, password=False):
        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.configure(fg="#222")
                if password:
                    entry.configure(show="*")

        def on_focus_out(e):
            if entry.get().strip() == "":
                entry.insert(0, placeholder)
                entry.configure(fg="#9aa3ad")
                if password:
                    entry.configure(show="")

        entry.insert(0, placeholder)
        entry.configure(fg="#9aa3ad")
        if password:
            entry.configure(show="")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
