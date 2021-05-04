"""This script stores global variables."""
import json


class Variables:
    def __init__(self):
        self.users = {}

    def load_users(self):
        with open("users.txt") as users:
            for user in users:
                (username, password) = user.split()
                self.users[username] = password

    def get_users(self):
        # Initialize the users dictionary if its empty.
        # If it's not empty, return the dict.
        if len(self.users) == 0:
            self.load_users()
        return self.users



