# kots_interface/trainee_view_window.py
import sqlite3
import tkinter as tk
from tkinter import ttk  # For Treeview
from data import database

class TraineeViewWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("View Trainees")

        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Novice Status", "Role"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Novice Status", text="Novice Status")
        self.tree.heading("Role", text="Role")
        self.tree.pack(padx=10, pady=10)

        self.load_trainees()

    def load_trainees(self):
        conn = database.DBConnection.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trainees")
            trainees = cursor.fetchall()
            for trainee in trainees:
                novice_status = "Novice" if trainee[2] == 1 else "Experienced"
                formatted_trainee = (trainee[0], trainee[1], novice_status, trainee[3])
                self.tree.insert("", tk.END, values=formatted_trainee)
        except sqlite3.Error as e:
            tk.messagebox.showerror("Database Error", f"Error loading trainees: {e}")
        finally:
            conn.close()