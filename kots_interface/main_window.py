import tkinter as tk
from .register_trainee_window import RegisterTraineeWindow
from .trainee_view_window import TraineeViewWindow
from .register_many_trainees_window import RegisterManyTraineesWindow


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Kots")

        self.root.geometry("800x600")

        register_button = tk.Button(root, text="Register Trainee", command=self.open_register_trainee)
        register_button.pack()

        view_trainees_button = tk.Button(root, text="View Trainees", command=self.open_trainee_view)
        view_trainees_button.pack()

    def open_register_trainee(self):
        register_window = tk.Toplevel(self.root)
        RegisterTraineeWindow(register_window)

    def open_trainee_view(self):
        view_window = tk.Toplevel(self.root)
        TraineeViewWindow(view_window)

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()