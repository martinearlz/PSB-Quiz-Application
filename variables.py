"""This script stores global variables."""
import os
import sys
import json


class Variables:
    def __init__(self):
        self.users = {}
        self.questions = ()
        self.options = ()
        self.answers = ()
        
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    def load_users(self):
        with open(self.resource_path("databases/users.txt")) as users:
            for user in users:
                (username, password) = user.split()
                self.users[username] = password
            
    def get_users(self):
        # Initialize the users dictionary if its empty.
        # If it's not empty, return the dict.
        if len(self.users) == 0:
            self.load_users()
        return self.users

    def load_quiz(self):
        with open(self.resource_path("databases/quiz.json")) as quiz:
            data = json.load(quiz)
        self.questions = data['question']
        self.options = data['options']
        self.answers = data['answer']

    def get_questions(self):
        if len(self.questions) == 0:
            self.load_quiz()
        return self.questions

    def get_options(self):
        if len(self.options) == 0:
            self.load_quiz()
        return self.options

    def get_answers(self):
        if len(self.answers) == 0:
            self.load_quiz()
        return self.answers
    
    def get_scores(self):
        with open(self.resource_path('databases/high_scores.txt'), 'r') as score_file:
             scores = score_file.readlines()
        return scores
