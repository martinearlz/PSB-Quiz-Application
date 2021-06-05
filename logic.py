"""This script stores the train logic class that contains all the program-related functions."""
from variables import Variables

variables = Variables()


class Logic:
    def __init__(self):
        self.username = ""
        
    def login(self, username, password):
        # Load the users dictionary,
        users = variables.get_users()
        # If the username is not in the dictionary, then return false (prevents exceptions).
        if username not in users:
            return False
        # Else, if the username is in the dictionary, just
        # check whether the value is the same as the password enter.
        if users[username] == password:
            self.username = username
            return True
        return False
    
    def get_current_user_name(self):
        return self.username
        

class Quiz:
    def __init__(self):
        self.correct_answers = 0
        self.answers = variables.get_answers()
        self.questions = variables.get_questions()
        self.options = variables.get_options()
        self.has_initialized = False
        self.answer_map = {1 : "A", 2 : "B", 3 : "C", 4 : "D"}

    def mark_answer(self, answer, q_no):
        '''
        Marks the given answer for the given question number.

        Args:
        - answer (int) : The answer that the user gave.
        - q_no (int) : The question number.

        Returns:
        - none
        '''
        if answer == self.answers[q_no]:
            self.correct_answers += 1

    def get_results(self):
        '''
        Returns the results of an attempt.

        Args:
        - none

        Returns:
        - correct_answers (int) : number of correct answers.
        - wrong_answers (int) : number of wrong answers.
        - score (int) : score.
        '''
        # calculates the wrong count
        wrong_answers = len(self.questions) - self.correct_answers
        # calculates the percentage of correct answers
        score = self.correct_answers / len(self.questions) * 100
        return self.correct_answers, wrong_answers, score

    def is_end_of_quiz(self, q_no):
        '''
        Checks whether the quiz is already at the end.

        Args:
        - q_no (int) : Current question number.

        Returns:
        - is_end_of_quiz (bool) : True if the quiz is already at the end. False otherwise.
        '''
        return q_no == len(self.questions)

    def load_options(self, opts, q_no):
        '''
        Loads options to the radio button.

        Args:
        - opts (radio button) : Options.
        - q_no (int) : Current question number.

        Returns:
        - none
        '''
        for val, option in enumerate(self.options[q_no]):
            opts[val]['text'] = f"{self.answer_map[val+1]}. {option}"

    def get_current_question(self, q_no):
        '''
        Returns the current question text for the given question number.

        Args:
        - q_no (int) : Question number.

        Returns:
        - question (str) : The question.
        '''
        return self.questions[q_no]

    def get_correct_answers(self):
        return self.correct_answers

    def reset_answers(self):
        self.correct_answers = 0
    
    def get_questions(self):
        return self.questions
    
    def get_answers(self):
        answers = list(map(lambda x: self.answer_map[x], self.answers))
        return answers
