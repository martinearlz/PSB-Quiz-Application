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
    
    def get_user_scores(self):
        scores = variables.get_scores()

        # Create a new list to assign value from LINES list, based on the current username.
        user_scores = list(filter(lambda score: self.username in score, scores))
        
        # return last 3 in the list
        return user_scores[-3:]
    
    def get_high_scores(self):
        # Get the last 10 scores
        scores = variables.get_scores()[-10:]
        # Sort from highest to lowest.
        scores.sort(reverse=True, key=lambda x: int(''.join(filter(str.isdigit, x))))
        return scores
    
    def save_user_score(self, score):
        with open("high_scores.txt", "a+") as score_file:
            score_file.write(f"{self.username} {score}\n")

class Quiz:
    def __init__(self):
        self.correct_answers = 0
        self.user_answers = []
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
        self.user_answers.append(answer)
        
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
        score = int(self.correct_answers / len(self.questions) * 100)
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
        self.user_answers.clear()
    
    def get_questions(self):
        return self.questions
    
    def get_answers(self):
        answers = list(map(lambda x: self.answer_map[x], self.answers))
        return answers
    
    def get_corrections(self):
        corrected_list = []
        
        if not self.user_answers:
            return corrected_list
        
        # For every answer for each question,
        for index, correct_answer in enumerate(self.answers):
            answer = self.user_answers[index]
            # Skip records where the user's answer is correct.
            if answer == correct_answer:
                continue
            
            # Check whether the answer is above 0, and gets the answer from the options list. Otherwise, the user did not answer.
            if answer > 0:
                users_answer = self.options[index][answer - 1]
            else:
                users_answer = "empty"
                
            corrected_list.append(f"For question {index + 1}, your answer is: {users_answer}. The correct answer is: {self.options[index][correct_answer - 1]}")
            
        if not corrected_list:
            corrected_list.append("You got it all correct!")
            
        return corrected_list
