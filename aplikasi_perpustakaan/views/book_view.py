import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from controllers.book_controller import (
    create_book, fetch_books, edit_book, remove_book
)
from controllers.category_controller import fetch_categories
import os

class BookView:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD Buku - Perpustakaan Digital")
        self.root.geometry("900x550")
        self.root.configure(bg="#f4f6f9")

        self.selected_id = None
        self.image_path = None

        # ===== HEADER =====
        header = tk.Frame(root, bg="#1976d2", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="📘 Manajemen Buku",
            bg="#1976d2",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=15)

        # ===== CONTENT =====
        content = tk.Frame(root, bg="#f4f6f9")
        content.pack(expand=True, fill="both")

        card = tk.Frame(content, bg="white", padx=30, pady=25)
        card.pack(pady=30)

        tk.Label(
            card,
            text="Data Buku",
            bg="white",
            font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # ===== FORM =====
        # Arrange inputs in two columns
        tk.Label(card, text="Judul Buku", bg="white").grid(row=0, column=0, sticky="w")
        tk.Label(card, text="Nama Penulis", bg="white").grid(row=2, column=0, sticky="w")
        tk.Label(card, text="Jumlah Stok", bg="white").grid(row=0, column=1, sticky="w")

        self.e_title = tk.Entry(card, width=35)
        self.e_author = tk.Entry(card, width=35)
        self.e_stock = tk.Entry(card, width=15)

        self.e_title.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.e_author.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.e_stock.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(card, text="Kategori", bg="white").grid(row=4, column=0, sticky="w")
        self.cb_category = ttk.Combobox(card, width=32, state="readonly")
        self.cb_category.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # ===== COVER / Preview =====
        preview_frame = tk.Frame(card, bg="#f0f0f0", width=140, height=170)
        preview_frame.grid(row=0, column=2, rowspan=4, padx=(40,0), pady=5)
        preview_frame.grid_propagate(False)
        self.image_preview = tk.Label(preview_frame, bg="#f0f0f0", text="Preview\nGambar",
                                      fg="#999", font=("Segoe UI", 10))
        self.image_preview.pack(fill="both", expand=True)

        tk.Label(card, text="Cover Buku", bg="white").grid(row=4, column=0, sticky="w", pady=5)
        tk.Button(
            card,
            text="Pilih Gambar",
            bg="#607d8b",
            fg="white",
            relief="flat",
            command=self.choose_image
        ).grid(row=4, column=1, sticky="w")

        # ===== BUTTONS =====
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Tambah", bg="#1976d2", fg="white",
                  width=10, command=self.add).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Update", bg="#388e3c", fg="white",
                  width=10, command=self.update).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="Delete", bg="#d32f2f", fg="white",
                  width=10, command=self.delete).grid(row=0, column=2, padx=5)

        # ===== LIST =====
        self.listbox = tk.Listbox(card, width=90, height=8)
        self.listbox.grid(row=6, column=0, columnspan=3, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.select_item)

        self.refresh()

    def choose_image(self):
        file = filedialog.askopenfilename(
            title="Pilih Cover Buku",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if file:
            # Use project-root images directory (avoid depending on current working dir)
            try:
                from pathlib import Path
                import shutil

                project_root = Path(__file__).resolve().parent.parent
                images_dir = project_root.joinpath('images')
                images_dir.mkdir(parents=True, exist_ok=True)

                filename = os.path.basename(file)
                dest_path = images_dir.joinpath(filename)
                dest = str(dest_path)

                # Try copying; if fails, try creating parent and retry
                try:
                    if not dest_path.exists():
                        shutil.copy2(file, dest)
                except Exception as e_copy:
                    try:
                        images_dir.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file, dest)
                    except Exception as e2:
                        # Show debug info to help diagnose path issues
                        src_exists = os.path.exists(file)
                        info = (
                            f"Gagal menyalin gambar: {e2}\n"
                            f"Sumber ada: {src_exists}\n"
                            f"Sumber: {file}\n"
                            f"Dest (dir): {images_dir}\n"
                            f"Dest (file): {dest}"
                        )
                        messagebox.showerror('Gagal menyalin gambar', info)
                        # Fallback: use original absolute path if readable
                        if src_exists:
                            self.image_path = os.path.abspath(file)
                        return

                # Store absolute path to copied image
                self.image_path = os.path.abspath(dest)
            except Exception as e:
                messagebox.showerror('Error', f"Error processing image: {e}")
                return

    def add(self):
        title = self.e_title.get().strip()
        author = self.e_author.get().strip()
        stock_str = self.e_stock.get().strip()
        
        if not title or not author or not stock_str:
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        
        try:
            stock = int(stock_str)
            if stock < 0:
                messagebox.showerror("Error", "Stok tidak boleh negatif!")
                return
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka!")
            return
        
        # determine category id
        cat_sel = self.cb_category.get().strip()
        category_id = None
        if cat_sel:
            try:
                category_id = int(cat_sel.split(" - ", 1)[0])
            except Exception:
                category_id = None

        create_book(title, author, stock, self.image_path, category_id)
        messagebox.showinfo("Sukses", "Buku berhasil ditambahkan!")
        self.clear()
        self.refresh()

    def select_item(self, event):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        data = fetch_books()[index]

        # data: id, title, author, stock, image_path, category_id
        self.selected_id = data[0]
        self.e_title.delete(0, tk.END)
        self.e_author.delete(0, tk.END)
        self.e_stock.delete(0, tk.END)

        self.e_title.insert(0, data[1])
        self.e_author.insert(0, data[2])
        self.e_stock.insert(0, data[3])
        try:
            cid = data[5]
            if cid is None:
                self.cb_category.set("")
            else:
                # find category label
                cats = fetch_categories()
                for c in cats:
                    if c[0] == cid:
                        self.cb_category.set(f"{c[0]} - {c[1]}")
                        break
        except Exception:
            pass

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih buku terlebih dahulu!")
            return
        
        title = self.e_title.get().strip()
        author = self.e_author.get().strip()
        stock_str = self.e_stock.get().strip()
        
        if not title or not author or not stock_str:
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        
        try:
            stock = int(stock_str)
            if stock < 0:
                messagebox.showerror("Error", "Stok tidak boleh negatif!")
                return
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka!")
            return
        
        # determine category id
        cat_sel = self.cb_category.get().strip()
        category_id = None
        if cat_sel:
            try:
                category_id = int(cat_sel.split(" - ", 1)[0])
            except Exception:
                category_id = None

        edit_book(
            self.selected_id,
            title,
            author,
            stock,
            category_id
        )
        messagebox.showinfo("Sukses", "Buku berhasil diperbarui!")
        self.clear()
        self.refresh()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih buku terlebih dahulu!")
            return
        
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus buku ini?"):
            remove_book(self.selected_id)
            messagebox.showinfo("Sukses", "Buku berhasil dihapus!")
            self.clear()
            self.refresh()

    def clear(self):
        self.selected_id = None
        self.image_path = None
        self.e_title.delete(0, tk.END)
        self.e_author.delete(0, tk.END)
        self.e_stock.delete(0, tk.END)
        try:
            self.cb_category.set("")
        except Exception:
            pass

    def refresh(self):
        self.listbox.delete(0, tk.END)
        # populate category combobox
        try:
            cats = fetch_categories()
            options = [f"{c[0]} - {c[1]}" for c in cats]
            self.cb_category['values'] = options
        except Exception:
            self.cb_category['values'] = []

        for b in fetch_books():
            self.listbox.insert(
                tk.END,
                f"ID:{b[0]} | Judul:{b[1]} | Penulis:{b[2]} | Stok:{b[3]}"
            )
