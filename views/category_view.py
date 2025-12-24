import tkinter as tk
from tkinter import messagebox
from controllers.category_controller import (
    create_category,
    fetch_categories,
    edit_category,
    remove_category
)

class CategoryView:
    def __init__(self, root):
        self.root = root
        self.root.title("Kelola Kategori")
        self.root.geometry("500x400")
        self.root.configure(bg="#f4f6f9")

        self.selected_id = None

        # ===== HEADER =====
        header = tk.Frame(root, bg="#1976d2", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="📂 Kelola Kategori Buku",
            bg="#1976d2",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=15)

        # ===== CONTENT =====
        card = tk.Frame(root, bg="white", padx=20, pady=20)
        card.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            card,
            text="Nama Kategori",
            bg="white",
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        self.entry_name = tk.Entry(card, width=40)
        self.entry_name.pack(pady=5)

        # ===== BUTTONS =====
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Tambah",
            bg="#1976d2",
            fg="white",
            width=10,
            command=self.add
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Update",
            bg="#388e3c",
            fg="white",
            width=10,
            command=self.update
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Delete",
            bg="#d32f2f",
            fg="white",
            width=10,
            command=self.delete
        ).grid(row=0, column=2, padx=5)

        # ===== LIST =====
        self.listbox = tk.Listbox(card, height=8)
        self.listbox.pack(fill="both", expand=True, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.select_item)

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for c in fetch_categories():
            self.listbox.insert(tk.END, f"{c[0]} - {c[1]}")

    def add(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning("Peringatan", "Nama kategori tidak boleh kosong!")
            return
        
        create_category(name)
        messagebox.showinfo("Sukses", "Kategori berhasil ditambahkan!")
        self.clear()
        self.refresh()

    def select_item(self, event):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        data = fetch_categories()[index]
        self.selected_id = data[0]
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, data[1])

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih kategori terlebih dahulu!")
            return
        
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning("Peringatan", "Nama kategori tidak boleh kosong!")
            return
        
        edit_category(self.selected_id, name)
        messagebox.showinfo("Sukses", "Kategori berhasil diperbarui!")
        self.clear()
        self.refresh()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih kategori terlebih dahulu!")
            return
        
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus kategori ini?"):
            remove_category(self.selected_id)
            messagebox.showinfo("Sukses", "Kategori berhasil dihapus!")
            self.clear()
            self.refresh()

    def clear(self):
        self.selected_id = None
        self.entry_name.delete(0, tk.END)
