import tkinter as tk
from tkinter import OptionMenu, messagebox
from data import database

class RegisterTraineeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Register Trainee")


        self.root.geometry("800x600")

        self.name_label = tk.Label(root, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.clicked = tk.StringVar()
        role_options = ["Debater", "Adjudicator"]
        self.clicked.set("Debater")

 
        self.role_label = tk.Label(root, text="Role:")
        self.role_label.pack()
        self.role_drop = tk.OptionMenu(root, self.clicked, *role_options) 
        self.role_drop.pack()

        self.register_button = tk.Button(root, text="Register", command=self.register)
        self.register_button.pack()

    def register(self):
        name = self.name_entry.get()
        role = self.clicked.get()
        conn = database.DBConnection.create_connection()
        try:
            database.DatabaseFunctions.register_trainee(conn, name, role)
            messagebox.showinfo("Success", "Trainee registered!")
        except Exception as e:
            messagebox.showerror("Error", f"Error registering trainee: {e}")
        finally:
            conn.close()