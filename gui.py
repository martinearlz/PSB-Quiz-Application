"""This script stores the train logic class that contains all the program-related functions."""

# Initialize libraries needed for the program.
import tkinter as tk
from tkinter import ttk, messagebox
from logic import Logic

logic = Logic()


class MainController(tk.Tk):
    """
    This class is the main controller for the tkinter frames
    (Login Page, Dashboard) in the program.
    Acts as a superclass too, containing several variables that'll be used
    in each subclass (frames).
    """

    def __init__(self, *args, **kwargs):
        # Initialize a class that inherits the Tk module.
        tk.Tk.__init__(self, *args, **kwargs)
        # Create a frame container that'll be used to show
        # Multiple frames (pages) that is going to be used for the program.
        frame_containers = tk.Frame(self)
        frame_containers.pack(side="top", fill="both", expand=True)
        frame_containers.grid_rowconfigure(0, weight=1)
        frame_containers.grid_columnconfigure(0, weight=1)

        # Custom TKinter style.
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure(
            'flat.TButton', borderwidth=0, background='#038579', foreground="#ffffff")
        self.style.map('flat.TButton',
                       foreground=[('disabled', 'yellow'),
                                   ('pressed', '#a4a6a5'),
                                   ('active', '#e3e8e6')],
                       background=[('active', '#0e5e34')])

        # Magic!
        self.frames = {}

        for pages in (Login, Dashboard):
            frames = pages(frame_containers, self)
            self.frames[pages] = frames
            frames.grid(row=0, column=0, sticky="nsew")

        # Initially show the login page.
        self.show_frame(Login)

    def show_frame(self, page):
        self.frames[page].tkraise()


class Login(tk.Frame):
    """
    This class is the login page of the program.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#009688')
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # The big title in front with y paddings of 20 and x paddings of 50
        program_title = tk.Label(self, text="PSB Quiz", font="Arial 50", background='#009688',
                                 foreground="#fff")
        program_title.pack(pady=20, padx=50)

        # Login form inputs.
        username_input = ttk.Entry(self, width=30, style="flat.TButton")
        username_input.pack(padx=50)
        username_input.insert(0, "Username")

        password_input = ttk.Entry(self, width=30, style="flat.TButton")
        password_input.pack(padx=50, pady=10)
        password_input.insert(0, "Password")

        # Login button, which then triggers the private login method.
        login_btn = ttk.Button(self, text="Log in",
                               command=lambda: self.__login(
                                   username_input.get(), password_input.get()),
                               style='flat.TButton',
                               width=30)
        login_btn.pack(pady=5)

    def __login(self, username, password):
        # If the login was unsuccessful,
        if not logic.login(username, password):
            # Show an error and return (to prevent the show frame from executing).
            tk.messagebox.showerror(
                "Error!", "Username or password is incorrect.")
            return
        self.controller.show_frame(Dashboard)


class Dashboard(tk.Frame):
    """
    This class is the main page of the program.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#009688')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        program_title = tk.Label(self, text="Dashboard", font="Arial 30", background='#009688',
                                 foreground="#fff")
        program_title.pack(pady=35, padx=10)


def main():
    program = MainController()
    program.title("PSB Quiz")
    program.mainloop()


if __name__ == "__main__":
    main()
