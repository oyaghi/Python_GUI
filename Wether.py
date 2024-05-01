import tkinter as tk
from tkinter import messagebox
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("Weather.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Report (id INTEGER PRIMARY KEY, date DATE, title TEXT, subject TEXT, text TEXT)")
        # self.cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)", ("ali", "1500")) Add it in order to have a valid user
        self.conn.commit()

    def verify_user(self, username, password):
        self.cur.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
        return self.cur.fetchone()

    def save_report(self, date, title, subject, text):
        self.cur.execute("INSERT INTO Report (date, title, subject, text) VALUES (?, ?, ?, ?)", (date, title, subject, text))
        self.conn.commit()

class LoginPage:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.geometry("400x400")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root, textvariable=self.username_var)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, textvariable=self.password_var, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        user = self.db.verify_user(username, password)
        if user:
            self.root.destroy()
            DetailPage(user)
        else:
            messagebox.showerror("Error", "Incorrect username or password")

class DetailPage:
    def __init__(self, user):
        self.user = user

        self.root = tk.Tk()
        self.root.title("Detail Page")
        self.root.geometry("400x400")

        self.date_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.subject_var = tk.StringVar()
        self.text_var = tk.StringVar()

        self.date_label = tk.Label(self.root, text="Date:")
        self.date_label.pack()
        self.date_entry = tk.Entry(self.root, textvariable=self.date_var)
        self.date_entry.pack()

        self.title_label = tk.Label(self.root, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.root, textvariable=self.title_var)
        self.title_entry.pack()

        self.subject_label = tk.Label(self.root, text="Subject:")
        self.subject_label.pack()
        self.subject_entry = tk.Entry(self.root, textvariable=self.subject_var)
        self.subject_entry.pack()

        self.text_label = tk.Label(self.root, text="Text:")
        self.text_label.pack()
        self.text_entry = tk.Entry(self.root, textvariable=self.text_var)
        self.text_entry.pack()

        self.save_button = tk.Button(self.root, text="Save", command=self.save_report)
        self.save_button.pack()

        self.cancel_button = tk.Button(self.root, text="Cancel", command=self.clear_fields)
        self.cancel_button.pack()

        self.modify_button = tk.Button(self.root, text="Modify", command=self.open_edit_page)
        self.modify_button.pack()

        self.previous_button = tk.Button(self.root, text="Previous", command=self.go_back)
        self.previous_button.pack()

        self.root.mainloop()

    def save_report(self):
        date = self.date_var.get()
        title = self.title_var.get()
        subject = self.subject_var.get()
        text = self.text_var.get()

        if not (date and title and subject and text):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        db.save_report(date, title, subject, text)
        messagebox.showinfo("Success", "Report saved successfully")

    def clear_fields(self):
        self.date_var.set("")
        self.title_var.set("")
        self.subject_var.set("")
        self.text_var.set("")

    def open_edit_page(self):
        self.root.withdraw()
        EditPage(self.user, self.root)

    def go_back(self):
        self.root.destroy()
        root = tk.Tk()
        root.title("Login Page")
        LoginPage(root, db)

class EditPage:
    def __init__(self, user, previous_root):
        self.user = user
        self.previous_root = previous_root
        

        self.root = tk.Toplevel(self.previous_root)
        self.root.title("Edit Page")

        # Set the size of the window
        self.root.geometry("400x400")

        self.records = self.get_records_from_db()

        self.record_var = tk.StringVar()
        self.record_var.set(self.records[0])  # Set default value

        self.record_label = tk.Label(self.root, text="Select Record:")
        self.record_label.pack()
        self.record_dropdown = tk.OptionMenu(self.root, self.record_var, *self.records)
        self.record_dropdown.pack()

        self.load_button = tk.Button(self.root, text="Load Record", command=self.load_record)
        self.load_button.pack()

        self.date_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.subject_var = tk.StringVar()
        self.text_var = tk.StringVar()

        self.date_label = tk.Label(self.root, text="Date:")
        self.date_label.pack()
        self.date_entry = tk.Entry(self.root, textvariable=self.date_var)
        self.date_entry.pack()

        self.title_label = tk.Label(self.root, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.root, textvariable=self.title_var)
        self.title_entry.pack()

        self.subject_label = tk.Label(self.root, text="Subject:")
        self.subject_label.pack()
        self.subject_entry = tk.Entry(self.root, textvariable=self.subject_var)
        self.subject_entry.pack()

        self.text_label = tk.Label(self.root, text="Text:")
        self.text_label.pack()
        self.text_entry = tk.Entry(self.root, textvariable=self.text_var)
        self.text_entry.pack()

        self.save_button = tk.Button(self.root, text="Save Changes", command=self.save_changes)
        self.save_button.pack()

        self.delete_button = tk.Button(self.root, text="Delete Record", command=self.delete_record)
        self.delete_button.pack()

        self.back_button = tk.Button(self.root, text="Previous", command=self.go_back)
        self.back_button.pack()

    def get_records_from_db(self):
        db.cur.execute("SELECT id FROM Report")
        return [record[0] for record in db.cur.fetchall()]

    def load_record(self):
        record_id = self.record_var.get()
        db.cur.execute("SELECT * FROM Report WHERE id = ?", (record_id,))
        record = db.cur.fetchone()
        if record:
            self.date_var.set(record[1])
            self.title_var.set(record[2])
            self.subject_var.set(record[3])
            self.text_var.set(record[4])
        else:
            messagebox.showerror("Error", "Record not found")

    def save_changes(self):
        record_id = self.record_var.get()
        date = self.date_var.get()
        title = self.title_var.get()
        subject = self.subject_var.get()
        text = self.text_var.get()

        db.cur.execute("UPDATE Report SET date=?, title=?, subject=?, text=? WHERE id=?", (date, title, subject, text, record_id))
        db.conn.commit()
        messagebox.showinfo("Success", "Changes saved successfully")

    def delete_record(self):
        record_id = self.record_var.get()
        db.cur.execute("DELETE FROM Report WHERE id = ?", (record_id,))
        db.conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully")

    def go_back(self):
        self.root.destroy()
        DetailPage(self.user)

if __name__ == "__main__":
    db = Database()
    root = tk.Tk()
    root.title("Login Page")
    LoginPage(root, db)
    root.mainloop()
