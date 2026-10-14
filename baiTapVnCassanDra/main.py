import tkinter as tk
from tkinter import ttk, messagebox
from queries import CassandraQueries


class CassandraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management - Cassandra")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        try:
            self.db = CassandraQueries()
        except Exception as e:
            messagebox.showerror(
                "Lỗi kết nối Cassandra",
                f"Không thể kết nối Astra DB:\n\n{e}"
            )
            self.root.destroy()
            return

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_ui()

    def create_ui(self):
        # =========================
        # Tiêu đề
        # =========================
        title = ttk.Label(
            self.root,
            text="HOTEL MANAGEMENT - CASSANDRA",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=(15, 5))

        subtitle = ttk.Label(
            self.root,
            text="Các chức năng Q1 → Q5 và thống kê",
            font=("Segoe UI", 10)
        )
        subtitle.pack(pady=(0, 15))

        # =========================
        # Khu vực chức năng
        # =========================
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=5)

        self.q1_frame = ttk.Frame(notebook)
        self.q2_frame = ttk.Frame(notebook)
        self.q3_frame = ttk.Frame(notebook)
        self.q4_frame = ttk.Frame(notebook)
        self.q5_frame = ttk.Frame(notebook)
        self.stat_frame = ttk.Frame(notebook)

        notebook.add(self.q1_frame, text="Q1 - Khách sạn")
        notebook.add(self.q2_frame, text="Q2 - Phòng")
        notebook.add(self.q3_frame, text="Q3 - Lịch sử đặt")
        notebook.add(self.q4_frame, text="Q4 - Booking theo ngày")
        notebook.add(self.q5_frame, text="Q5 - Hóa đơn")
        notebook.add(self.stat_frame, text="Thống kê")

        self.build_q1()
        self.build_q2()
        self.build_q3()
        self.build_q4()
        self.build_q5()
        self.build_statistics()

    # =========================
    # Helper
    # =========================
    def add_input(self, parent, label, row, default=""):
        ttk.Label(parent, text=label).grid(
            row=row, column=0, padx=10, pady=10, sticky="w"
        )

        entry = ttk.Entry(parent, width=45)
        entry.grid(
            row=row, column=1, padx=10, pady=10, sticky="w"
        )

        if default:
            entry.insert(0, default)

        return entry

    def create_tree(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(frame, show="headings")

        vertical = ttk.Scrollbar(
            frame, orient="vertical", command=tree.yview
        )
        horizontal = ttk.Scrollbar(
            frame, orient="horizontal", command=tree.xview
        )

        tree.configure(
            yscrollcommand=vertical.set,
            xscrollcommand=horizontal.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        return tree

    def display_rows(self, tree, rows):
        tree.delete(*tree.get_children())

        if not rows:
            messagebox.showinfo("Kết quả", "Không tìm thấy dữ liệu.")
            return

        # Lấy tên cột từ object Row Cassandra
        columns = rows[0]._fields

        tree["columns"] = columns

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=150, anchor="center")

        for row in rows:
            values = []

            for column in columns:
                value = getattr(row, column)
                values.append(str(value) if value is not None else "")

            tree.insert("", "end", values=values)

    # =========================
    # Q1
    # =========================
    def build_q1(self):
        form = ttk.Frame(self.q1_frame)
        form.pack(fill="x", padx=20, pady=20)

        self.q1_hotel_id = self.add_input(
            form, "Hotel ID:", 0, "HTL001"
        )

        ttk.Button(
            form,
            text="Tìm khách sạn",
            command=self.run_q1
        ).grid(row=0, column=2, padx=15)

        self.q1_tree = self.create_tree(self.q1_frame)

    def run_q1(self):
        try:
            hotel_id = self.q1_hotel_id.get().strip()

            if not hotel_id:
                raise ValueError("Vui lòng nhập Hotel ID.")

            rows = self.db.get_hotel(hotel_id)
            self.display_rows(self.q1_tree, rows)

        except Exception as e:
            messagebox.showerror("Q1 - Lỗi", str(e))

    # =========================
    # Q2
    # =========================
    def build_q2(self):
        form = ttk.Frame(self.q2_frame)
        form.pack(fill="x", padx=20, pady=20)

        self.q2_hotel_id = self.add_input(
            form, "Hotel ID:", 0, "HTL001"
        )

        self.q2_available = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            form,
            text="Chỉ hiển thị phòng AVAILABLE",
            variable=self.q2_available
        ).grid(row=1, column=1, sticky="w", padx=10, pady=5)

        ttk.Button(
            form,
            text="Tìm phòng",
            command=self.run_q2
        ).grid(row=0, column=2, padx=15)

        self.q2_tree = self.create_tree(self.q2_frame)

    def run_q2(self):
        try:
            hotel_id = self.q2_hotel_id.get().strip()

            if not hotel_id:
                raise ValueError("Vui lòng nhập Hotel ID.")

            rows = self.db.get_rooms(
                hotel_id,
                self.q2_available.get()
            )

            self.display_rows(self.q2_tree, rows)

        except Exception as e:
            messagebox.showerror("Q2 - Lỗi", str(e))

    # =========================
    # Q3
    # =========================
    def build_q3(self):
        form = ttk.Frame(self.q3_frame)
        form.pack(fill="x", padx=20, pady=20)

        self.q3_guest_id = self.add_input(
            form, "Guest ID:", 0, "GUEST001"
        )

        ttk.Button(
            form,
            text="Xem lịch sử",
            command=self.run_q3
        ).grid(row=0, column=2, padx=15)

        self.q3_tree = self.create_tree(self.q3_frame)

    def run_q3(self):
        try:
            guest_id = self.q3_guest_id.get().strip()

            if not guest_id:
                raise ValueError("Vui lòng nhập Guest ID.")

            rows = self.db.get_guest_bookings(guest_id)
            self.display_rows(self.q3_tree, rows)

        except Exception as e:
            messagebox.showerror("Q3 - Lỗi", str(e))

    # =========================
    # Q4
    # =========================
    def build_q4(self):
        form = ttk.Frame(self.q4_frame)
        form.pack(fill="x", padx=20, pady=20)

        self.q4_hotel_id = self.add_input(
            form, "Hotel ID:", 0, "HTL001"
        )

        self.q4_start = self.add_input(
            form, "Ngày bắt đầu:", 1, "2026-10-01"
        )

        self.q4_end = self.add_input(
            form, "Ngày kết thúc:", 2, "2026-10-31"
        )

        ttk.Button(
            form,
            text="Tra cứu",
            command=self.run_q4
        ).grid(row=0, column=2, rowspan=3, padx=15)

        ttk.Label(
            self.q4_frame,
            text="Định dạng ngày: YYYY-MM-DD"
        ).pack(anchor="w", padx=20)

        self.q4_tree = self.create_tree(self.q4_frame)

    def run_q4(self):
        try:
            hotel_id = self.q4_hotel_id.get().strip()
            start_date = self.q4_start.get().strip()
            end_date = self.q4_end.get().strip()

            if not hotel_id:
                raise ValueError("Vui lòng nhập Hotel ID.")

            rows = self.db.get_hotel_bookings_by_date(
                hotel_id,
                start_date,
                end_date
            )

            self.display_rows(self.q4_tree, rows)

        except Exception as e:
            messagebox.showerror("Q4 - Lỗi", str(e))

    # =========================
    # Q5
    # =========================
    def build_q5(self):
        form = ttk.Frame(self.q5_frame)
        form.pack(fill="x", padx=20, pady=20)

        self.q5_booking_id = self.add_input(
            form,
            "Booking UUID:",
            0,
            "3f2504e0-4f89-11d3-9a0c-0305e82c3301"
        )

        ttk.Button(
            form,
            text="Tra cứu hóa đơn",
            command=self.run_q5
        ).grid(row=0, column=2, padx=15)

        self.q5_tree = self.create_tree(self.q5_frame)

    def run_q5(self):
        try:
            booking_id = self.q5_booking_id.get().strip()

            if not booking_id:
                raise ValueError("Vui lòng nhập Booking UUID.")

            rows = self.db.get_invoice_by_booking(booking_id)
            self.display_rows(self.q5_tree, rows)

        except Exception as e:
            messagebox.showerror("Q5 - Lỗi", str(e))

    # =========================
    # Statistics
    # =========================
    def build_statistics(self):
        form = ttk.Frame(self.stat_frame)
        form.pack(fill="x", padx=20, pady=20)

        self.stat_hotel_id = self.add_input(
            form, "Hotel ID:", 0, "HTL001"
        )

        ttk.Button(
            form,
            text="Thống kê",
            command=self.run_statistics
        ).grid(row=0, column=2, padx=15)

        self.stat_text = tk.Text(
            self.stat_frame,
            height=12,
            font=("Consolas", 12)
        )
        self.stat_text.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    def run_statistics(self):
        try:
            hotel_id = self.stat_hotel_id.get().strip()

            if not hotel_id:
                raise ValueError("Vui lòng nhập Hotel ID.")

            result = self.db.get_room_statistics(hotel_id)

            self.stat_text.delete("1.0", tk.END)

            self.stat_text.insert(
                tk.END,
                f"THỐNG KÊ KHÁCH SẠN: {hotel_id}\n"
                f"{'=' * 50}\n\n"
                f"Số lượng phòng      : {result['room_count']}\n"
                f"Giá phòng cao nhất  : {result['max_price']}\n"
                f"Giá phòng thấp nhất  : {result['min_price']}\n"
            )

        except Exception as e:
            messagebox.showerror("Thống kê - Lỗi", str(e))

    def on_close(self):
        try:
            self.db.close()
        except Exception:
            pass

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CassandraApp(root)
    root.mainloop()
