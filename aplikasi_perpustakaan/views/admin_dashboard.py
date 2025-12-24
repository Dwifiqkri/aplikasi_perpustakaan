import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from views.book_view import BookView
from controllers.book_controller import create_book, fetch_books, edit_book, remove_book
from controllers.category_controller import (
    create_category,
    fetch_categories,
    edit_category,
    remove_category,
)

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard Admin - Perpustakaan Digital")
        self.root.geometry("1400x800")
        self.root.configure(bg="#ffffff")
        
        self.current_view = "books"
        self.books = []
        self.selected_id = None
        self.image_path = None
        
        # Create main container with sidebar
        main_container = tk.Frame(root, bg="#ffffff")
        main_container.pack(fill="both", expand=True)
        
        # Create sidebar
        self.create_sidebar(main_container)
        
        # Create main content area
        self.content_frame = tk.Frame(main_container, bg="#ffffff")
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Show initial view
        self.show_books_view()

    def create_sidebar(self, parent):
        """Create the sidebar with navigation"""
        sidebar = tk.Frame(parent, bg="#22252a", width=220)
        sidebar.pack(side="left", fill="y", padx=0, pady=0)
        sidebar.pack_propagate(False)

        # Top brand
        top_brand = tk.Frame(sidebar, bg="#111214", height=60)
        top_brand.pack(fill="x")
        tk.Label(top_brand, text="One It Library", bg="#111214", fg="white", 
                font=("Segoe UI", 12, "bold")).pack(padx=12, pady=12)

        # Avatar section
        avatar = tk.Frame(sidebar, bg="#2b2f33", height=120)
        avatar.pack(fill="x")
        tk.Label(avatar, text="\n", bg="#2b2f33").pack()
        tk.Label(avatar, text="🙂", bg="#2b2f33", font=("Segoe UI Emoji", 40)).pack(pady=10)
        tk.Label(avatar, text="Admin", bg="#2b2f33", fg="white", font=("Segoe UI", 10)).pack()

        # Menu items
        menu = tk.Frame(sidebar, bg="#22252a")
        menu.pack(fill="both", expand=True, pady=20)

        menu_items = [
            ("🏠  Dashboard", self.show_dashboard_view),
            ("📂  Kategori Buku", self.show_category_view),
            ("📚  Data Buku", self.show_books_view),
            ("🔁  Transaksi", self.show_loan_view),
        ]

        for text, cmd in menu_items:
            btn = tk.Button(menu, text=text, anchor="w", bg="#22252a", fg="#dfe6e9", 
                           bd=0, relief="flat", padx=14, pady=12, font=("Segoe UI", 10),
                           activebackground="#2b2f33", activeforeground="#ffffff", command=cmd)
            btn.pack(fill="x")

        # Footer with logout
        footer = tk.Frame(sidebar, bg="#22252a")
        footer.pack(fill="x", side="bottom", padx=12, pady=12)
        tk.Button(footer, text="Logout", bg="#c0392b", fg="white", bd=0, relief="flat",
                 padx=12, pady=8, font=("Segoe UI", 10), command=self.logout).pack(fill="x")

    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard_view(self):
        """Show main dashboard"""
        self.clear_content()
        self.current_view = "dashboard"
        
        main = tk.Frame(self.content_frame, bg="#ffffff")
        main.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(main, text="Dashboard", bg="#ffffff", fg="#222", 
                font=("Segoe UI", 24, "bold")).pack(pady=(0, 30))
        
        # Summary cards
        cards_frame = tk.Frame(main, bg="#ffffff")
        cards_frame.pack(fill="x", pady=20)
        
        stats = [
            ("Total Buku", "150", "#2e86de"),
            ("Total Anggota", "45", "#27ae60"),
            ("Buku Dipinjam", "23", "#f39c12"),
            ("Transaksi Hari Ini", "8", "#9b59b6"),
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(main, bg=color, highlightthickness=0)
            card.pack(side="left", padx=15, pady=10, fill="both", expand=True)
            card.configure(height=120)
            
            tk.Label(card, text=value, bg=color, fg="white", 
                    font=("Segoe UI", 28, "bold")).pack(pady=(15, 5))
            tk.Label(card, text=label, bg=color, fg="white", 
                    font=("Segoe UI", 11)).pack()

    def show_category_view(self):
        """Show category management view embedded in admin dashboard"""
        self.clear_content()
        self.current_view = "categories"

        main = tk.Frame(self.content_frame, bg="#ffffff")
        main.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(main, text="Kategori Buku", bg="#ffffff", fg="#222",
                font=("Segoe UI", 20, "bold")).pack(pady=(0, 20), anchor="w")

        card = tk.Frame(main, bg="#ffffff")
        card.pack(fill="both", expand=True)

        form_frame = tk.Frame(card, bg="#ffffff")
        form_frame.pack(anchor="n", pady=10, padx=10, fill="x")

        tk.Label(form_frame, text="Nama Kategori", bg="#ffffff", fg="#333",
                font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.cv_category_name = tk.Entry(form_frame, width=40, font=("Segoe UI", 10))
        self.cv_category_name.pack(pady=(5, 10), anchor="w")

        btn_frame = tk.Frame(form_frame, bg="#ffffff")
        btn_frame.pack(pady=(0, 10), anchor="w")

        tk.Button(btn_frame, text="Tambah", bg="#2e86de", fg="white", width=10,
                 bd=0, relief="flat", font=("Segoe UI", 10, "bold"),
                 command=self.add_category_action).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", bg="#27ae60", fg="white", width=10,
                 bd=0, relief="flat", font=("Segoe UI", 10, "bold"),
                 command=self.update_category_action).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", bg="#c0392b", fg="white", width=10,
                 bd=0, relief="flat", font=("Segoe UI", 10, "bold"),
                 command=self.delete_category_action).grid(row=0, column=2, padx=5)

        # Listbox for categories
        list_frame = tk.Frame(card, bg="#ffffff")
        list_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        self.category_listbox = tk.Listbox(list_frame, height=10, font=("Segoe UI", 10))
        self.category_listbox.pack(side="left", fill="both", expand=True)
        self.category_listbox.bind("<<ListboxSelect>>", self.select_category)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.category_listbox.yview)
        self.category_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.refresh_categories()

    def refresh_categories(self):
        try:
            self.category_listbox.delete(0, tk.END)
            for c in fetch_categories():
                self.category_listbox.insert(tk.END, f"{c[0]} - {c[1]}")
        except Exception:
            pass

    def add_category_action(self):
        name = self.cv_category_name.get().strip()
        if not name:
            messagebox.showwarning("Peringatan", "Nama kategori tidak boleh kosong!")
            return
        try:
            create_category(name)
            messagebox.showinfo("Sukses", "Kategori berhasil ditambahkan!")
            self.clear_category_inputs()
            self.refresh_categories()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah kategori: {e}")

    def select_category(self, event):
        if not self.category_listbox.curselection():
            return
        index = self.category_listbox.curselection()[0]
        try:
            data = fetch_categories()[index]
            self.selected_category_id = data[0]
            self.cv_category_name.delete(0, tk.END)
            self.cv_category_name.insert(0, data[1])
        except Exception:
            pass

    def update_category_action(self):
        if not getattr(self, 'selected_category_id', None):
            messagebox.showwarning("Peringatan", "Pilih kategori terlebih dahulu!")
            return
        name = self.cv_category_name.get().strip()
        if not name:
            messagebox.showwarning("Peringatan", "Nama kategori tidak boleh kosong!")
            return
        try:
            edit_category(self.selected_category_id, name)
            messagebox.showinfo("Sukses", "Kategori berhasil diperbarui!")
            self.clear_category_inputs()
            self.refresh_categories()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui kategori: {e}")

    def delete_category_action(self):
        if not getattr(self, 'selected_category_id', None):
            messagebox.showwarning("Peringatan", "Pilih kategori terlebih dahulu!")
            return
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus kategori ini?"):
            try:
                remove_category(self.selected_category_id)
                messagebox.showinfo("Sukses", "Kategori berhasil dihapus!")
                self.clear_category_inputs()
                self.refresh_categories()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus kategori: {e}")

    def clear_category_inputs(self):
        self.selected_category_id = None
        try:
            self.cv_category_name.delete(0, tk.END)
        except Exception:
            pass

    def show_books_view(self):
        """Show books management view"""
        self.clear_content()
        self.current_view = "books"
        
        main = tk.Frame(self.content_frame, bg="#ffffff")
        main.pack(fill="both", expand=True, padx=30, pady=20)

        # Title
        tk.Label(main, text="DATA Buku", bg="#ffffff", fg="#222", 
                font=("Segoe UI", 20, "bold")).pack(pady=(0, 25), anchor="w")

        # Form area with two columns (left: inputs, right: image preview)
        form_container = tk.Frame(main, bg="#ffffff")
        form_container.pack(anchor="n", pady=10, fill="x")

        # Left: two-column input grid
        inputs_frame = tk.Frame(form_container, bg="#ffffff")
        inputs_frame.pack(side="left", padx=(0, 40), fill="x", expand=True)

        left_col = tk.Frame(inputs_frame, bg="#ffffff")
        right_col = tk.Frame(inputs_frame, bg="#ffffff")
        left_col.grid(row=0, column=0, sticky="nw", padx=(0, 40))
        right_col.grid(row=0, column=1, sticky="ne")

        # Left column fields
        tk.Label(left_col, text="Judul Buku", bg="#ffffff", fg="#333",
            font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.cv_title = tk.Entry(left_col, width=40, font=("Segoe UI", 10))
        self.cv_title.grid(row=1, column=0, pady=(4, 12), sticky="w")

        tk.Label(left_col, text="Nama Penulis", bg="#ffffff", fg="#333",
            font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w")
        self.cv_author = tk.Entry(left_col, width=40, font=("Segoe UI", 10))
        self.cv_author.grid(row=3, column=0, pady=(4, 12), sticky="w")

        # Right column fields
        tk.Label(right_col, text="Jumlah Stok", bg="#ffffff", fg="#333",
            font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.cv_stock = tk.Entry(right_col, width=20, font=("Segoe UI", 10))
        self.cv_stock.grid(row=1, column=0, pady=(4, 12), sticky="w")

        tk.Label(right_col, text="Kategori", bg="#ffffff", fg="#333",
            font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w")
        self.cv_category = ttk.Combobox(right_col, width=28, state="readonly")
        self.cv_category.grid(row=3, column=0, pady=(4, 12), sticky="w")

        tk.Label(right_col, text="Penerbit", bg="#ffffff", fg="#333",
            font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w")
        self.cv_publisher = tk.Entry(right_col, width=40, font=("Segoe UI", 10))
        self.cv_publisher.grid(row=5, column=0, pady=(4, 12), sticky="w")

        tk.Label(right_col, text="Tahun Terbit", bg="#ffffff", fg="#333",
            font=("Segoe UI", 10, "bold")).grid(row=6, column=0, sticky="w")
        self.cv_year = tk.Entry(right_col, width=15, font=("Segoe UI", 10))
        self.cv_year.grid(row=7, column=0, pady=(4, 12), sticky="w")

        # Cover controls under inputs (aligned left)
        cover_frame = tk.Frame(inputs_frame, bg="#ffffff")
        cover_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(6,0))
        tk.Label(cover_frame, text="Cover Buku", bg="#ffffff", fg="#333",
            font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.image_button = tk.Button(cover_frame, text="Pilih Gambar", bg="#708090", 
                          fg="white", bd=0, relief="flat", padx=15, pady=8,
                          font=("Segoe UI", 10), command=self.choose_image)
        self.image_button.pack(anchor="w", pady=(6,0))
        self.image_label = tk.Label(cover_frame, text="Belum ada gambar dipilih", 
                        bg="#ffffff", fg="#999", font=("Segoe UI", 9))
        self.image_label.pack(anchor="w", pady=(6,0))

        # Image preview
        image_preview_frame = tk.Frame(form_container, bg="#f0f0f0", width=150, height=180)
        image_preview_frame.pack(side="right", padx=(20, 0))
        image_preview_frame.pack_propagate(False)
        
        self.image_preview = tk.Label(image_preview_frame, bg="#f0f0f0", text="Preview\nGambar",
                                      fg="#999", font=("Segoe UI", 10))
        self.image_preview.pack(fill="both", expand=True)

        # Action buttons
        actions_frame = tk.Frame(main, bg="#ffffff")
        actions_frame.pack(pady=20)
        
        tk.Button(actions_frame, text="Tambah", bg="#2e86de", fg="white", width=12,
                 bd=0, relief="flat", font=("Segoe UI", 10, "bold"), padx=10, pady=8,
                 command=self.add_book_action).pack(side="left", padx=5)
        tk.Button(actions_frame, text="Update", bg="#27ae60", fg="white", width=12,
                 bd=0, relief="flat", font=("Segoe UI", 10, "bold"), padx=10, pady=8,
                 command=self.update_book_action).pack(side="left", padx=5)
        tk.Button(actions_frame, text="Delete", bg="#c0392b", fg="white", width=12,
                 bd=0, relief="flat", font=("Segoe UI", 10, "bold"), padx=10, pady=8,
                 command=self.delete_book_action).pack(side="left", padx=5)

        # Separator
        separator = tk.Frame(main, bg="#e0e0e0", height=2)
        separator.pack(fill="x", pady=15)

        # Data table with search and pagination
        table_header = tk.Frame(main, bg="#ffffff")
        table_header.pack(fill="x", pady=(10, 15))

        # Pagination and search
        pagination_frame = tk.Frame(table_header, bg="#ffffff")
        pagination_frame.pack(side="left")
        
        tk.Label(pagination_frame, text="10 ", bg="#ffffff", fg="#666", 
                font=("Segoe UI", 9)).pack(side="left")
        ttk.Combobox(pagination_frame, values=["10", "25", "50"], width=3, state="readonly").pack(side="left", padx=(0, 5))
        tk.Label(pagination_frame, text="records per page", bg="#ffffff", fg="#666",
                font=("Segoe UI", 9)).pack(side="left")

        search_frame = tk.Frame(table_header, bg="#ffffff")
        search_frame.pack(side="right")
        tk.Label(search_frame, text="Search:", bg="#ffffff", fg="#666",
                font=("Segoe UI", 9)).pack(side="left", padx=(0, 8))
        self.search_entry = tk.Entry(search_frame, width=20, font=("Segoe UI", 9))
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_books_filtered())

        # Table frame
        table_frame = tk.Frame(main, bg="#ffffff")
        table_frame.pack(fill="both", expand=True)

        # Create treeview table (include Kategori)
        columns = ("No", "Judul", "Pengarang", "Kategori", "Penerbit", "Tahun Terbit", "Jumlah Buku")
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show="headings")
        
        # Define column headings and widths
        column_config = [
            ("No", 30),
            ("Judul", 150),
            ("Pengarang", 120),
            ("Kategori", 120),
            ("Penerbit", 100),
            ("Tahun Terbit", 80),
            ("Jumlah Buku", 80),
        ]
        
        for col, width in column_config:
            self.tree.column(col, width=width)
            self.tree.heading(col, text=col)

        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), 
                       background="#f5f5f5", foreground="#333")
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=35)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Load books
        self.load_books()
        # populate categories into combobox
        try:
            cats = fetch_categories()
            self._category_map = {str(c[0]): c[1] for c in cats}
            options = [f"{c[0]} - {c[1]}" for c in cats]
            self.cv_category['values'] = options
        except Exception:
            self._category_map = {}
            self.cv_category['values'] = []

    def show_loan_view(self):
        """Show loan/transaction view"""
        self.clear_content()
        self.current_view = "loans"
        
        main = tk.Frame(self.content_frame, bg="#ffffff")
        main.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(main, text="Transaksi", bg="#ffffff", fg="#222",
                font=("Segoe UI", 20, "bold")).pack(pady=(0, 20), anchor="w")
        
        tk.Label(main, text="Fitur Transaksi sedang dalam pengembangan",
                bg="#ffffff", fg="#666", font=("Segoe UI", 12)).pack(pady=50)


    def load_books(self):
        """Load books into the table"""
        self.books = fetch_books()
        self.populate_table(self.books)

    def load_books_filtered(self):
        """Load books with search filter"""
        search_term = self.search_entry.get().lower()
        filtered_books = [b for b in self.books if search_term in str(b).lower()]
        self.populate_table(filtered_books)

    def populate_table(self, books):
        """Populate the treeview table with books"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        
        for idx, book in enumerate(books, 1):
            
            try:
                bid, title, author, stock, image_path, category_id, publisher, year = book
            except Exception:
                bid, title, author, stock, image_path, category_id = book
                publisher = None
                year = None
            category_name = "-"
            try:
                if category_id is not None:
                    category_name = self._category_map.get(str(category_id), "-")
            except Exception:
                category_name = "-"
            self.tree.insert("", "end", iid=str(bid), values=(
                idx,
                title[:30] + "..." if len(title) > 30 else title,
                author[:20] + "..." if len(author) > 20 else author,
                category_name,
                publisher or "-",
                year or "-",
                stock
            ))

    def on_row_select(self, event):
        """Handle selection of a row"""
        selection = self.tree.selection()
        if selection:
            item_id = selection[0]
            try:
                item_id = int(item_id)
                for book in self.books:
                    if book[0] == item_id:
                        self.selected_id = book[0]
                        self.cv_title.delete(0, tk.END)
                        self.cv_title.insert(0, book[1])
                        self.cv_author.delete(0, tk.END)
                        self.cv_author.insert(0, book[2])
                        self.cv_stock.delete(0, tk.END)
                        self.cv_stock.insert(0, str(book[3]))

                        try:
                            cid = book[5]
                            if cid is None:
                                self.cv_category.set("")
                            else:
                                label = f"{cid} - {self._category_map.get(str(cid), '')}" if hasattr(self, '_category_map') else str(cid)
                                self.cv_category.set(label)
                                self.selected_category_id = cid
                        except Exception:
                            pass
                        # set publisher and year if available
                        try:
                            # book tuple may include publisher and year at indices 6 and 7
                            if len(book) > 6:
                                pub = book[6] or ""
                            else:
                                pub = ""
                            if len(book) > 7:
                                yr = book[7] or ""
                            else:
                                yr = ""
                            try:
                                self.cv_publisher.delete(0, tk.END)
                                self.cv_publisher.insert(0, str(pub))
                            except Exception:
                                pass
                            try:
                                self.cv_year.delete(0, tk.END)
                                self.cv_year.insert(0, str(yr))
                            except Exception:
                                pass
                        except Exception:
                            pass

                        # Load and show image preview if available
                        try:
                            img_path = book[4] if len(book) > 4 else None
                            if img_path and os.path.exists(img_path):
                                img = Image.open(img_path)
                                img.thumbnail((140, 170))
                                photo = ImageTk.PhotoImage(img)
                                self.image_preview.config(image=photo, text="")
                                # keep reference to avoid GC
                                self.image_preview.image = photo
                                # update filename label and stored path
                                try:
                                    self.image_label.config(text=os.path.basename(img_path), fg="#333")
                                except Exception:
                                    pass
                                self.image_path = img_path
                            else:
                                # reset preview
                                self.image_preview.config(image="", text="Preview\nGambar")
                                try:
                                    self.image_label.config(text="Belum ada gambar dipilih", fg="#999")
                                except Exception:
                                    pass
                                self.image_path = None
                        except Exception as e:
                            print(f"Error loading preview image: {e}")
                        break
            except (ValueError, IndexError):
                pass

    def choose_image(self):
        """Open file dialog to choose image"""
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar Cover",
            filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
        )
        if file_path:
            self.image_path = file_path
            self.image_label.config(text=os.path.basename(file_path), fg="#333")
            # Show preview
            try:
                img = Image.open(file_path)
                img.thumbnail((140, 170))
                photo = ImageTk.PhotoImage(img)
                self.image_preview.config(image=photo, text="")
                self.image_preview.image = photo
            except Exception as e:
                print(f"Error loading image: {e}")

    def add_book_action(self):
        """Add a new book"""
        title = self.cv_title.get().strip()
        author = self.cv_author.get().strip()
        stock = self.cv_stock.get().strip() or "0"
        publisher = self.cv_publisher.get().strip()
        year = self.cv_year.get().strip()
        
        if not title or not author:
            messagebox.showerror("Error", "Judul dan Penulis harus diisi!")
            return
        
        try:
            stock_i = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Jumlah stok harus berupa angka!")
            return
        
        try:
            # determine selected category id
            cat_sel = self.cv_category.get().strip()
            category_id = None
            if cat_sel:
                try:
                    category_id = int(cat_sel.split(" - ", 1)[0])
                except Exception:
                    category_id = None

            create_book(title, author, stock_i, self.image_path or "", category_id, publisher, year)
            messagebox.showinfo("Success", "Buku berhasil ditambahkan!")
            self.clear_inputs()
            self.load_books()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah buku: {str(e)}")

    def update_book_action(self):
        """Update selected book"""
        if not self.selected_id:
            messagebox.showwarning("Warning", "Pilih buku yang ingin diupdate!")
            return
        
        title = self.cv_title.get().strip()
        author = self.cv_author.get().strip()
        stock = self.cv_stock.get().strip() or "0"
        publisher = self.cv_publisher.get().strip()
        year = self.cv_year.get().strip()
        
        if not title or not author:
            messagebox.showerror("Error", "Judul dan Penulis harus diisi!")
            return
        
        try:
            stock_i = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Jumlah stok harus berupa angka!")
            return
        
        try:
            cat_sel = self.cv_category.get().strip()
            category_id = None
            if cat_sel:
                try:
                    category_id = int(cat_sel.split(" - ", 1)[0])
                except Exception:
                    category_id = None

            edit_book(self.selected_id, title, author, stock_i, category_id, publisher, year)
            messagebox.showinfo("Success", "Buku berhasil diupdate!")
            self.clear_inputs()
            self.load_books()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengupdate buku: {str(e)}")

    def delete_book_action(self):
        """Delete selected book"""
        if not self.selected_id:
            messagebox.showwarning("Warning", "Pilih buku yang ingin dihapus!")
            return
        
        if messagebox.askyesno("Confirm", "Apakah Anda yakin ingin menghapus buku ini?"):
            try:
                remove_book(self.selected_id)
                messagebox.showinfo("Success", "Buku berhasil dihapus!")
                self.clear_inputs()
                self.load_books()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus buku: {str(e)}")

    def clear_inputs(self):
        """Clear all input fields"""
        self.cv_title.delete(0, tk.END)
        self.cv_author.delete(0, tk.END)
        self.cv_stock.delete(0, tk.END)
        self.cv_publisher.delete(0, tk.END)
        self.cv_year.delete(0, tk.END)
        try:
            self.cv_category.set("")
        except Exception:
            pass
        self.image_path = None
        self.image_label.config(text="Belum ada gambar dipilih", fg="#999")
        self.image_preview.config(image="", text="Preview\nGambar")
        self.selected_id = None

    def logout(self):
        """Logout and return to login screen"""
        from views.login_view import LoginView
        self.root.destroy()
        root = tk.Tk()
        LoginView(root)
        root.mainloop()
