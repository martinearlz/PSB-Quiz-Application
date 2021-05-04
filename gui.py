"""This script stores the train logic class that contains all the program-related functions."""

# Initialize libraries needed for the program.
import json
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

        for pages in (Login, Dashboard, QuestionPage):
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
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        program_title = tk.Label(self, text="Dashboard", font="Arial 30", background='#009688',
                                 foreground="#fff")
        program_title.pack(pady=35, padx=10)

        start_btn = ttk.Button(self, text="Start Quiz",
                               command=lambda: self.controller.show_frame(QuestionPage))
        start_btn.pack(pady=5)


class QuestionPage(tk.Frame):
    """
    This class is the QuestionPage of the program.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#009688')
        self.opt_selected = tk.IntVar()
        self.opts = self.radio_buttons()
        self.q_no = 0
        self.correct = 0
        self.data_size = len(question)
        self.controller = controller


    def display_result(self):
        # calculates the wrong count
        wrong_count = self.data_size - self.correct
        correct = f"Correct: {self.correct}"
        wrong = f"Wrong: {wrong_count}"

        # calcultaes the percentage of correct answers
        score = int(self.correct / self.data_size * 100)
        result = f"Score: {score}%"

        # Shows a message box to display the result
        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")

        # This method checks the Answer after we click on Next.

    def check_ans(self, q_no):

        # checks for if the selected option is correct
        if self.opt_selected.get() == answer[q_no]:
            # if the option is correct it return true
            return True

        # This method is used to check the answer of the
        # current question by calling the check_ans and question no.
        # if the question is correct it increases the count by 1
        # and then increase the question number by 1. If it is last
        # question then it calls display result to show the message box.
        # otherwise shows next question.

    def next_btn(self):

        # Check if the answer is correct
        if self.check_ans(self.q_no):
            # if the answer is correct it increments the correct by 1
            self.correct += 1

        # Moves to next Question by incrementing the q_no counter
        self.q_no += 1

        # checks if the q_no size is equal to the data size
        if self.q_no == self.data_size:

            # if it is correct then it displays the score
            self.display_result()

            # destroys the GUI
            self.destroy()
        else:
            # shows the next question
            self.display_question()
            self.display_options()

        # This method shows the two buttons on the screen.
        # The first one is the next_button which moves to next question
        # It has properties like what text it shows the functionality,
        # size, color, and property of text displayed on button. Then it
        # mentions where to place the button on the screen. The second
        # button is the exit button which is used to close the GUI without
        # completing the quiz.

    def buttons(self):

        # The first button is the Next button to move to the
        # next Question
        next_button = tk.Button(self, text="Next", command=self.next_btn,
                             width=10, bg="blue", fg="white", font=("ariel", 16, "bold"))

        # palcing the button  on the screen
        next_button.place(x=350, y=380)

        # This is the second button which is used to Quit the GUI
        quit_button = tk.Button(self, text="Quit", command=self.destroy,
                             width=5, bg="black", fg="white", font=("ariel", 16, " bold"))

        # placing the Quit button on the screen
        quit_button.place(x=700, y=50)

        # This method deselect the radio button on the screen
        # Then it is used to display the options available for the current
        # question which we obtain through the question number and Updates
        # each of the options for the current question of the radio button.

    def display_options(self):
        val = 0

        # deselecting the options
        self.opt_selected.set(0)

        # looping over the options to be displayed for the
        # text of the radio buttons.
        for option in options[self.q_no]:
            self.opts[val]['text'] = option
            val += 1

        # This method shows the current Question on the screen

    def display_question(self):

        # setting the Quetion properties
        q_no = tk.Label(self, text=question[self.q_no], width=60,
                     font=('ariel', 16, 'bold'), anchor='w')

        # placing the option on the screen
        q_no.place(x=70, y=100)


    def radio_buttons(self):

        # initialize the list with an empty list of options
        q_list = []

        # position of the first option
        y_pos = 150

        # adding the options to the list
        while len(q_list) < 4:
            # setting the radio button properties
            radio_btn = tk.Radiobutton(self, text=" ", variable=self.opt_selected,
                                       value=len(q_list) + 1, font=("ariel", 14))

            # adding the button to the list
            q_list.append(radio_btn)

            # placing the button
            radio_btn.place(x=100, y=y_pos)

            # incrementing the y-axis position by 40
            y_pos += 40

        # return the radio buttons
        return q_list


with open('data.json') as f:
    data = json.load(f)

question = (data['question'])
options = (data['options'])
answer = (data['answer'])


def main():
    program = MainController()
    program.title("PSB Quiz")
    program.mainloop()


if __name__ == "__main__":
    main()

