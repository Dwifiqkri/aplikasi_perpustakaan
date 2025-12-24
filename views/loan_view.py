import tkinter as tk
from tkinter import messagebox

class LoanView:
    def __init__(self, root):
        self.root = root
        self.root.title("Peminjaman Buku - Perpustakaan Digital")
        self.root.geometry("600x400")
        self.root.configure(bg="#f4f6f9")

        # ===== HEADER =====
        header = tk.Frame(root, bg="#1976d2", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="📚 Peminjaman Buku",
            bg="#1976d2",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=15)

        # ===== CONTENT =====
        card = tk.Frame(root, bg="white", padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card,
            text="Fitur Peminjaman Buku",
            bg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)

        tk.Label(
            card,
            text="Fitur ini masih dalam pengembangan",
            bg="white",
            font=("Segoe UI", 11),
            fg="#999"
        ).pack(pady=10)

        tk.Button(
            card,
            text="Tutup",
            bg="#d32f2f",
            fg="white",
            width=15,
            command=self.root.destroy
        ).pack(pady=20)
