import tkinter as tk
from tkinter import messagebox, ttk

students = []
selected_student_id = None
next_student_id = 1
root = None
username_entry = None
password_entry = None
name_entry = None
age_entry = None
class_entry = None
email_entry = None
search_entry = None
student_tree = None


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def validate_admin_credentials(username, password):
    return bool(username) and bool(password)


def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if not username or not password:
        messagebox.showwarning("Missing information", "Please enter both username and password.")
        return
    if validate_admin_credentials(username, password):
        show_student_manager()


def reset_form():
    global selected_student_id
    selected_student_id = None
    for entry in (name_entry, age_entry, class_entry, email_entry):
        entry.delete(0, tk.END)
    student_tree.selection_remove(student_tree.selection())


def refresh_student_table(filtered_students=None):
    for row in student_tree.get_children():
        student_tree.delete(row)
    records = filtered_students if filtered_students is not None else students
    for student in records:
        student_tree.insert(
            "",
            "end",
            iid=student["id"],
            values=(student["id"], student["name"], student["age"], student["class"], student["email"]),
        )


def get_form_values():
    values = (
        name_entry.get().strip(),
        age_entry.get().strip(),
        class_entry.get().strip(),
        email_entry.get().strip(),
    )
    if not all(values):
        messagebox.showwarning("Missing information", "Please fill in all student fields.")
        return None
    if not values[1].isdigit() or int(values[1]) <= 0:
        messagebox.showwarning("Invalid age", "Please enter a valid numeric age.")
        return None
    return values


def add_student():
    global next_student_id
    values = get_form_values()
    if values is None:
        return
    name, age, class_name, email = values
    students.append({"id": next_student_id, "name": name, "age": age, "class": class_name, "email": email})
    next_student_id += 1
    refresh_student_table()
    reset_form()
    messagebox.showinfo("Student added", "Student has been added successfully.")


def update_student():
    if selected_student_id is None:
        messagebox.showwarning("No selection", "Please select a student to update.")
        return
    values = get_form_values()
    if values is None:
        return
    for student in students:
        if student["id"] == selected_student_id:
            student.update(dict(zip(("name", "age", "class", "email"), values)))
            break
    refresh_student_table()
    reset_form()
    messagebox.showinfo("Student updated", "Student information has been updated.")


def delete_student():
    global selected_student_id
    if selected_student_id is None:
        messagebox.showwarning("No selection", "Please select a student to delete.")
        return
    if not messagebox.askyesno("Delete student", "Are you sure you want to delete this student?"):
        return
    students[:] = [student for student in students if student["id"] != selected_student_id]
    selected_student_id = None
    refresh_student_table()
    reset_form()


def search_students():
    query = search_entry.get().strip().lower()
    if not query:
        refresh_student_table()
        return
    matching = [student for student in students if query in student["name"].lower() or query in student["email"].lower()]
    refresh_student_table(matching)


def on_tree_select(event):
    global selected_student_id
    selected = student_tree.selection()
    if not selected:
        return
    selected_student_id = int(selected[0])
    student = next(student for student in students if student["id"] == selected_student_id)
    for entry, key in ((name_entry, "name"), (age_entry, "age"), (class_entry, "class"), (email_entry, "email")):
        entry.delete(0, tk.END)
        entry.insert(0, student[key])


def logout():
    global selected_student_id
    selected_student_id = None
    students.clear()
    build_ui()


def show_student_manager():
    global name_entry, age_entry, class_entry, email_entry, search_entry, student_tree
    root.title("Student Management System")
    root.geometry("1040x650")
    root.minsize(860, 560)
    clear_frame(root)

    header = ttk.Frame(root, style="Header.TFrame", padding=(30, 24, 30, 18))
    header.pack(fill="x")
    ttk.Label(header, text="Student Management System", style="HeaderTitle.TLabel").pack(anchor="w")
    ttk.Label(header, text="Keep your student records organized and up to date.", style="HeaderSubtitle.TLabel").pack(anchor="w", pady=(4, 0))

    toolbar = ttk.Frame(root, padding=(30, 18, 30, 14))
    toolbar.pack(fill="x")
    search_box = ttk.Frame(toolbar, style="Search.TFrame")
    search_box.pack(side="left", fill="x", expand=True, padx=(0, 12))
    search_entry = ttk.Entry(search_box, style="Search.TEntry")
    search_entry.pack(side="left", fill="x", expand=True)
    ttk.Button(search_box, text="Search", style="Accent.TButton", command=search_students).pack(side="left", padx=(8, 0))
    ttk.Button(toolbar, text="Clear", command=lambda: [search_entry.delete(0, tk.END), refresh_student_table()]).pack(side="left")
    ttk.Button(toolbar, text="Log out", style="Quiet.TButton", command=logout).pack(side="right", padx=(12, 0))

    content = ttk.Frame(root, padding=(30, 0, 30, 28))
    content.pack(fill="both", expand=True)
    form = ttk.Labelframe(content, text="  STUDENT DETAILS  ", style="Card.TLabelframe", padding=(20, 18))
    form.pack(side="left", fill="y", padx=(0, 18), pady=(0, 10))
    fields = ("Full name", "Age", "Class", "Email address")
    entries = []
    for row, label in enumerate(fields):
        ttk.Label(form, text=label, style="Field.TLabel").grid(row=row * 2, column=0, sticky="w", pady=(0, 6))
        entry = ttk.Entry(form, width=28)
        entry.grid(row=row * 2 + 1, column=0, pady=(0, 12))
        entries.append(entry)
    name_entry, age_entry, class_entry, email_entry = entries
    buttons = ttk.Frame(form)
    buttons.grid(row=8, column=0, sticky="ew", pady=(10, 0))
    ttk.Button(buttons, text="Add student", style="Accent.TButton", command=add_student).grid(row=0, column=0, sticky="ew")
    ttk.Button(buttons, text="Update student", command=update_student).grid(row=1, column=0, sticky="ew", pady=(8, 0))
    ttk.Button(buttons, text="Delete student", style="Danger.TButton", command=delete_student).grid(row=2, column=0, sticky="ew", pady=(8, 0))
    ttk.Button(buttons, text="Clear form", style="Quiet.TButton", command=reset_form).grid(row=3, column=0, sticky="ew", pady=(8, 0))

    table_frame = ttk.Frame(content, style="Card.TFrame")
    table_frame.pack(side="left", fill="both", expand=True, pady=(0, 10))
    columns = ("ID", "Name", "Age", "Class", "Email")
    student_tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse", style="Records.Treeview")
    for column in columns:
        student_tree.heading(column, text=column)
        student_tree.column(column, anchor="center", width=110, stretch=True)
    student_tree.column("Name", width=180, anchor="w")
    student_tree.column("Email", width=220, anchor="w")
    scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=student_tree.yview)
    scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=student_tree.xview)
    student_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    student_tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)
    student_tree.bind("<<TreeviewSelect>>", on_tree_select)
    refresh_student_table()


def build_ui():
    global root, username_entry, password_entry
    root = tk.Tk()
    root.title("Student Management Login")
    root.geometry("460x500")
    root.configure(bg="#eef3f7")
    root.resizable(False, False)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#eef3f7")
    style.configure("TLabel", background="#eef3f7", foreground="#334155", font=("Segoe UI", 10))
    style.configure("Header.TFrame", background="#123047")
    style.configure("HeaderTitle.TLabel", background="#123047", foreground="#ffffff", font=("Segoe UI", 23, "bold"))
    style.configure("HeaderSubtitle.TLabel", background="#123047", foreground="#b9d4dd", font=("Segoe UI", 10))
    style.configure("Field.TLabel", background="#ffffff", foreground="#334155", font=("Segoe UI", 10, "bold"))
    style.configure("TButton", padding=(12, 8), font=("Segoe UI", 10, "bold"), background="#dce7eb", foreground="#123047", borderwidth=0)
    style.map("TButton", background=[("active", "#c9dce2")])
    style.configure("Accent.TButton", background="#087f8c", foreground="#ffffff")
    style.map("Accent.TButton", background=[("active", "#066b76")])
    style.configure("Danger.TButton", background="#f6d8d6", foreground="#9f2f2a")
    style.configure("Quiet.TButton", background="#eef3f7", foreground="#52616b")
    style.configure("Search.TFrame", background="#ffffff")
    style.configure("Search.TEntry", padding=8, fieldbackground="#ffffff")
    style.configure("Card.TFrame", background="#ffffff")
    style.configure("Card.TLabelframe", background="#ffffff", foreground="#123047", bordercolor="#d5e0e5", relief="solid")
    style.configure("Card.TLabelframe.Label", background="#ffffff", foreground="#087f8c", font=("Segoe UI", 9, "bold"))
    style.configure("Records.Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#334155", rowheight=34, borderwidth=0, font=("Segoe UI", 10))
    style.configure("Records.Treeview.Heading", background="#e8f0f2", foreground="#123047", font=("Segoe UI", 9, "bold"), padding=9)
    style.map("Records.Treeview", background=[("selected", "#bde3e4")], foreground=[("selected", "#123047")])

    header = ttk.Frame(root, style="Header.TFrame", padding=(30, 30, 30, 24))
    header.pack(fill="x")
    ttk.Label(header, text="Welcome Back", style="HeaderTitle.TLabel").pack(anchor="w")
    ttk.Label(header, text="Login to access the student management system", style="HeaderSubtitle.TLabel").pack(anchor="w", pady=(4, 0))
    form = ttk.Frame(root, padding=(30, 24, 30, 30))
    form.pack(fill="both", expand=True)
    ttk.Label(form, text="Username", style="Field.TLabel").pack(anchor="w")
    username_entry = ttk.Entry(form, font=("Segoe UI", 11))
    username_entry.pack(fill="x", pady=(5, 16))
    ttk.Label(form, text="Password", style="Field.TLabel").pack(anchor="w")
    password_entry = ttk.Entry(form, show="*", font=("Segoe UI", 11))
    password_entry.pack(fill="x", pady=(5, 22))
    ttk.Button(form, text="Login to dashboard", style="Accent.TButton", command=login).pack(fill="x", ipady=4)
    ttk.Label(form, text="Demo credentials: bhimappa / bhimappa123", foreground="#64748b").pack(pady=(16, 0))
    username_entry.focus_set()
    root.bind("<Return>", lambda event: login())
    root.mainloop()


if __name__ == "__main__":
    build_ui()
