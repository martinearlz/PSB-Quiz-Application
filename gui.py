"""This script stores the train logic class that contains all the program-related functions."""

# Initialize libraries needed for the program.
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from logic import Logic, Quiz

logic = Logic()
quiz = Quiz()


class MainController(tk.Tk):
    """
    This class is the main controller for the tkinter frames
    (Login Page, Dashboard, Question Page, Results) in the program.
    Manages frames, navigations between frames, etc.
    """

    def __init__(self, *args, **kwargs):
        # Initialize a class that inherits the Tk module.
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("2000x2000")
        # Create a frame container that'll be used to show
        # Multiple frames (pages) that is going to be used for the program.
        self.frame_containers = tk.Frame(self)
        self.frame_containers.pack(side="top", fill="both", expand=True)
        self.frame_containers.grid_rowconfigure(0, weight=1)
        self.frame_containers.grid_columnconfigure(0, weight=1)

        # Custom TKinter styling.
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure(
            'flat.TButton', borderwidth=1, relief="groove", background='#ffffff', foreground="#000000")
        self.style.map('flat.TButton',
                       foreground=[('disabled', 'yellow'),
                                   ('pressed', '#a4a6a5'),
                                   ('active', '#e3e8e6')],
                       background=[('active', '#0e5e34')])

        self.frames = {}
        self.initialize_frames()

        # Initially show the login page.
        self.show_frame(Login)
        quiz.has_initialized = True

    def show_frame(self, page):
        self.frames[page].tkraise()

    def initialize_frames(self):
        for pages in (Login, Dashboard, QuestionPage, Results):
            frames = pages(self.frame_containers, self)
            self.frames[pages] = frames
            frames.grid(row=0, column=0, sticky="nsew")


class Login(tk.Frame):
    """
    This class is the login page of the program.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#ffffff')
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # The big title in front with y paddings of 20 and x paddings of 50
        self.program_title = tk.Label(
            self, text="PSB", font="Inter 60 bold", foreground="#B20437", background='#ffffff')
        self.program_title.place(relx=0.39, rely=0.35)
        self.program_title_2 = tk.Label(
            self, text="Quiz", font="Inter 60 bold", background='#ffffff')
        self.program_title_2.place(relx=0.49, rely=0.35)

        # Login form inputs.
        self.username_input = ttk.Entry(
            self, width=30, style="flat.TButton", font="Inter")
        self.username_input.place(relx=0.5, rely=0.5, anchor="center")
        self.username_input.insert(0, "Username")

        self.password_input = ttk.Entry(
            self, width=30, style="flat.TButton", font="Inter")
        self.password_input.place(relx=0.5, rely=0.56, anchor="center")
        self.password_input.insert(0, "Password")

        # Login button, which then triggers the private login method.
        self.login_btn = tk.Button(self, text="Log in",
                                   font="Inter 13 bold",
                                   command=lambda: self.__login(
                                       self.username_input.get(), self.password_input.get()),
                                   fg='#B20437',
                                   relief='groove',
                                   bg="white",
                                   width=30,
                                   height=2)

        self.login_btn.place(relx=0.5, rely=0.63, anchor="center")
        
        # Don't reinitialize the images if we already initialized it before.
        if quiz.has_initialized:
            return
        
        top_wave = Image.open("images/top_wave.png")
        top_wave = top_wave.resize((1280, 170), Image.ANTIALIAS)
        top_wave = ImageTk.PhotoImage(top_wave)
        self.top_wave_img = tk.Label(image=top_wave, background='#ffffff')
        self.top_wave_img.image = top_wave
        self.top_wave_img.place(x=-3, y=-3)

        bottom_wave = Image.open("images/bottom_wave.png")
        bottom_wave = bottom_wave.resize((1280, 170), Image.ANTIALIAS)
        bottom_wave = ImageTk.PhotoImage(bottom_wave)
        self.bottom_wave_img = tk.Label(
            image=bottom_wave, background='#ffffff')
        self.bottom_wave_img.image = bottom_wave
        self.bottom_wave_img.place(x=-3, y=508)

    def __login(self, username, password):
        # If the login was unsuccessful,
        if not logic.login(username, password):
            # Show an error and return (to prevent the show frame from executing).
            tk.messagebox.showerror(
                "Error!", "Username or password is incorrect.")
            return
        self.destroy()
        self.controller.initialize_frames()
        self.controller.show_frame(Dashboard)

    def destroy(self):
        self.program_title.destroy()
        self.program_title_2.destroy()
        self.username_input.destroy()
        self.password_input.destroy()
        self.login_btn.destroy()
        if hasattr(self, 'top_wave_img') and hasattr(self, 'bottom_wave_img'):
            self.top_wave_img.destroy()
            self.bottom_wave_img.destroy()
        super().destroy()


class Dashboard(tk.Frame):
    """
    This class is the main page of the program.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#ffffff')
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        program_title = tk.Label(
            self, text=f"👋 Welcome Back, {logic.get_current_user_name()}.", font="Inter 45", background='#ffffff')
        program_title.place(relx=0.05, rely=0.1)
        
        highscores_title = tk.Label(
            self, text=f"Recent Highscores", font="Inter 30 bold", background='#ffffff')
        highscores_title.place(relx=0.05, rely=0.24)
        
        quiz_title = tk.Label(
            self, text=f"CS PSB Quiz", font="Inter 30 bold", background='#ffffff')
        quiz_title.place(relx=0.7, rely=0.24)
        
        quiz_image = tk.Label(self, text=f"📗👨‍💻👩‍💻📘", font="Inter 70", background='#ffffff')
        quiz_image.place(relx=0.66, rely=0.35)
        
        quiz_description = tk.Text(self, wrap="word", font="Inter", foreground="#000000", background='#ffffff', width=35, bd=0, borderwidth=0, selectborderwidth=0, highlightthickness=0)
        quiz_description.insert("insert", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In vitae porttitor nulla. Maecenas auctor volutpat lectus, quis efficitur eros eleifend vel. Proin dignissim pretium eros eget bibendum. Integer rutrum leo nec orci feugiat accumsan. Integer elementum sem sed tincidunt rutrum. Phasellus porta quis libero ut varius. Nulla convallis auctor justo non porttitor. Vestibulum laoreet malesuada egestas.")
        quiz_description.configure(state='disabled')
        quiz_description.place(relx=0.67, rely=0.5)
        
        attempt_btn = tk.Button(self,
                                font="Inter 12 bold",
                                text="Attempt Quiz ➡️",
                               command=lambda: self.controller.show_frame(QuestionPage), 
                               width=33,
                               borderwidth=1,
                               fg='#B20437',
                               relief='groove',
                               highlightbackground="#ffffff")
        
        attempt_btn.place(relx=0.67, rely=0.73)

class QuestionPage(tk.Frame):
    """
    This class is the QuestionPage of the program.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#ffffff')
        self.controller = controller
        self.initialize()

    def display_result(self):
        correct_answers, wrong_answers, score = quiz.get_results()

        correct = f"Correct: {correct_answers}"
        wrong = f"Wrong: {wrong_answers}"

        # calcultaes the percentage of correct answers
        result = f"Score: {score}%"

        # Shows a message box to display the result
        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")

    def next_btn(self):
        # When the next button is clicked, destroy/remove the previous question to prevent overlapping.
        self.q_no.destroy()

        answer = self.opt_selected.get()
        quiz.mark_answer(answer, self.current_question)

        # Moves to next Question by incrementing the q_no counter
        self.current_question += 1

        # Checks whether the user is already at the end of the quiz,
        # displays the score of the user if true.
        if quiz.is_end_of_quiz(self.current_question):
            self.display_result()
            self.show_results()
            return

        # shows the next question
        self.display_question()
        self.display_options()

    def buttons(self):
        # The first button is the Next button to move to the
        # next Question
        self.next_button = tk.Button(self, text="Next Question ➡️", 
                                     command=self.next_btn, 
                                     font="Inter 14",
                                     width=20,
                                borderwidth=1,
                                fg='#B20437',
                                relief='groove',
                                highlightbackground="#ffffff",
                                bg="#ffffff")

        # palcing the button  on the screen
        self.next_button.place(relx=0.78, y=410)

        # This is the second button which is used to Quit the GUI
        self.quit_button = tk.Button(self, text="Quit 🏠", command=self.show_dashboard, font="Inter 14",
                               borderwidth=1,
                               height=2,
                               fg='#B20437',
                               relief='groove',
                               highlightbackground="#ffffff",
                               bg="#ffffff")
        

        # placing the Quit button on the screen
        self.quit_button.place(relx=0.055, rely=0.12)

    def show_dashboard(self):
        confirmation = messagebox.askyesno(
            "Confirmation", "Are you sure that you want to quit? All progress will be lost.")
        # If the user clicked no,
        if not confirmation:
            # return and do nothing.
            return
        self.destroy()
        self.initialize()
        quiz.reset_answers()
        self.controller.show_frame(Dashboard)

    def show_results(self):
        self.destroy()
        self.initialize()
        # Re-initialize frames to ensure the quiz instance used in the results page is updated.
        self.controller.initialize_frames()
        self.controller.show_frame(Results)

    def display_options(self):
        # deselecting the options
        self.opt_selected.set(0)
        quiz.load_options(self.opts, self.current_question)

    def display_question(self):
        tk.Label(
            self, text="👨‍💻 CS PSB Quiz 👩‍💻", font="Inter 50 bold", background='#ffffff').place(relx=0.35, rely=0.1)
        
        self.q_no = tk.Text(self, wrap="word", font="Inter 26", foreground="#000000", width=68, background='#ffffff', height=2, bd=0, borderwidth=0, selectborderwidth=0, highlightthickness=0)
        self.q_no.insert("insert", quiz.get_current_question(
            self.current_question))
        self.q_no.configure(state='disabled')
        self.q_no.place(x=70, y=180)
        
        tk.Label(
            self, text="Options:", font="Inter 24 bold", background='#ffffff').place(x=70, y=260)

    def radio_buttons(self):
        # initialize the list with an empty list of options
        option_list = []

        # Position of the first option
        y_pos = 310
        for i in range(0, 4):
            # setting the radio button properties
            radio_btn = tk.Radiobutton(self, text=" ", font="Inter 20", variable=self.opt_selected,
                                       value=i + 1, bg="#ffffff")
            # adding the button to the list
            option_list.append(radio_btn)
            # placing the button
            radio_btn.place(x=70, y=y_pos)
            # incrementing the y-axis position by 40
            y_pos += 40

        # return the radio buttons
        return option_list

    def initialize(self):
        # Then reinitialize them.
        self.current_question = 0
        self.opt_selected = tk.IntVar()
        self.opts = self.radio_buttons()
        self.display_question()
        self.display_options()
        self.buttons()

    def destroy(self):
        # Reset and destroy all widgets.
        for i in self.opts:
            i.destroy()
        self.opts = []
        self.q_no.destroy()
        self.next_button.destroy()
        self.quit_button.destroy()


class Results(tk.Frame):
    """
    This class shows the results page of the program.
    TODO (for part 2): 
    1. Show answers that the user got wrong and their corresponding correct answers.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#ffffff')
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.program_title = tk.Label(
            self, text="👨‍💻 CS PSB Quiz 👩‍💻", font="Inter 50 bold", background='#ffffff')
        self.program_title.place(relx=0.35, rely=0.1)
        self.show_score()
        self.show_misc()

    def show_score(self):
        self.label = tk.Label(self, text="You got:", font="Inter 28", background='#ffffff')
        self.label.place(relx=0.52, rely=0.3, anchor="center")

        score = quiz.get_results()[2]

        self.score_label = tk.Label(
            self, text=f"🎉 {score}% 🎉", font="Inter 34 bold", background='#ffffff', foreground="#1BB55C")
        self.score_label.place(relx=0.52, rely=0.4, anchor="center")

    def show_misc(self):
        # Shows other miscellaneous stuff such as buttons and labels.
        self.retake_btn = tk.Button(self, text="Retake Quiz ♻️", command=lambda: self.show_frame(
            QuestionPage), borderwidth=1,
                               fg='#B20437',
                               relief='groove',
                               highlightbackground="#ffffff")
        self.retake_btn.place(relx=0.8, rely=0.65)

        self.dashboard_btn = tk.Button(
            self, text="Finish 🏠", command=lambda: self.show_frame(Dashboard), borderwidth=1,
                               fg='#B20437',
                               relief='groove',
                               highlightbackground="#ffffff")
        self.dashboard_btn.place(relx=0.8, rely=0.71)

        self.question_answer_label = tk.Label(self, text=f"Review", font="Inter 26 bold", background='#ffffff',
                                              foreground="#000000")
        self.question_answer_label.place(relx=0.049, rely=0.59)

        self.question_answer_list = tk.Listbox(self, width=90)
        for index, questions in enumerate(quiz.get_questions()):
            self.question_answer_list.insert(
                index, f"{questions} : {quiz.get_answers()[index]}")
        self.question_answer_list.place(relx=0.05, rely=0.65)

    def show_frame(self, frame):
        self.destroy()
        self.controller.show_frame(frame)

    def destroy(self):
        quiz.reset_answers()
        self.program_title.destroy()
        self.label.destroy()
        self.score_label.destroy()
        self.retake_btn.destroy()
        self.dashboard_btn.destroy()


def main():
    program = MainController()
    program.title("PSB Quiz")
    program.mainloop()


if __name__ == "__main__":
    main()
