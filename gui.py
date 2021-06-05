"""This script stores the train logic class that contains all the program-related functions."""

# Initialize libraries needed for the program.
import tkinter as tk
from tkinter import ttk, messagebox
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
        
        self.frames = {}
        self.initialize_frames()
        
        # Initially show the login page.
        self.show_frame(Login)

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
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # The big title in front with y paddings of 20 and x paddings of 50
        program_title = tk.Label(self, text="PSB Quiz", font="Arial 50")
        program_title.place(relx=0.5, rely=0.4, anchor="center")

        # Login form inputs.
        username_input = ttk.Entry(self)
        username_input.place(relx=0.5, rely=0.5, anchor="center")
        username_input.insert(0, "Username")

        password_input = ttk.Entry(self)
        password_input.place(relx=0.5, rely=0.56, anchor="center")
        password_input.insert(0, "Password")

        # Login button, which then triggers the private login method.
        login_btn = ttk.Button(self, text="Log in",
                               command=lambda: self.__login(
                                   username_input.get(), password_input.get()))
        login_btn.place(relx=0.5, rely=0.63, anchor="center")

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
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        program_title = tk.Label(self, text="Dashboard", font="Arial 30")
        program_title.pack(pady=35, padx=10)

        start_btn = ttk.Button(self, text="Start Quiz",
                               command=lambda: self.controller.show_frame(QuestionPage))
        start_btn.pack(pady=5)


class QuestionPage(tk.Frame):
    """
    This class is the QuestionPage of the program.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
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
        self.next_button = ttk.Button(self, text="Next", command=self.next_btn,
                                      width=5)

        # palcing the button  on the screen
        self.next_button.place(relx=0.48, y=270)

        # This is the second button which is used to Quit the GUI
        self.quit_button = ttk.Button(self, text="Quit", command=self.show_dashboard,
                                      width=5)

        # placing the Quit button on the screen
        self.quit_button.place(relx=0.88, y=270)
        
    def show_dashboard(self):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure that you want to quit? All progress will be lost.")
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
        # setting the Question properties
        self.q_no = ttk.Label(self, text=quiz.get_current_question(
            self.current_question), font=("Arial", 18), anchor='w')
        # placing the option on the screen
        self.q_no.place(x=70, y=100)

    def radio_buttons(self):
        # initialize the list with an empty list of options
        option_list = []

        # Position of the first option
        y_pos = 150
        for i in range(0, 4):
            # setting the radio button properties
            radio_btn = tk.Radiobutton(self, text=" ", variable=self.opt_selected,
                                       value=i + 1, font=("Arial", 14))
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
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.program_title = tk.Label(self, text="Quiz Results", font="Arial 30")
        self.program_title.place(relx=0.5, rely=0.2, anchor="center")
        self.show_score()
        self.show_misc()
    
    def show_score(self):
        score = quiz.get_results()[2]
        
        self.score_label = tk.Label(self, text=f"{score}%", font="Arial 34 bold")
        self.score_label.place(relx=0.5, rely=0.4, anchor="center")
        
    def show_misc(self):
        # Shows other miscellaneous stuff such as buttons and labels.
        self.retake_btn = ttk.Button(self, text="Retake Quiz", command=lambda: self.show_frame(QuestionPage))
        self.retake_btn.place(relx=0.8, rely=0.65)
        
        self.dashboard_btn = ttk.Button(self, text="Finish", command=lambda: self.show_frame(Dashboard))
        self.dashboard_btn.place(relx=0.9, rely=0.65)
        
        self.question_answer_label = tk.Label(self, text=f"Accurate Answers", font="Arial 20")
        self.question_answer_label.place(relx=0.05, rely=0.6)
        
        self.question_answer_list = tk.Listbox(self)
        for index, questions in enumerate(quiz.get_questions()):
            self.question_answer_list.insert(index, f"{questions} : {quiz.get_answers()[index]}")
        self.question_answer_list.place(relx=0.05, rely=0.65)
    
    def show_frame(self, frame):
        self.destroy()
        self.controller.show_frame(frame)
        
    def destroy(self):
        quiz.reset_answers()
        self.program_title.destroy()
        self.score_label.destroy()
        self.retake_btn.destroy()
        self.dashboard_btn.destroy()
        
def main():
    program = MainController()
    program.title("PSB Quiz")
    program.mainloop()

if __name__ == "__main__":
    main()
