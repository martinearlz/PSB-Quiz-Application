"""This script stores global variables."""
import json
import os
root_dir = os.path.abspath(os.path.dirname(__file__))


class Variables:
    def __init__(self):
        self.users = {}
        self.questions = ()
        self.options = ()
        self.answers = ()

    def load_users(self):
        with open(root_dir+"/databases/users.txt") as users:
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
        with open(root_dir+"/databases/quiz.json") as quiz:
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
