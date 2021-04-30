"""This script stores the train logic class that contains all the program-related functions."""
from variables import Variables

variables = Variables()


class Logic:
    def login(self, username, password):
        # Load the users dictionary,
        users = variables.get_users()
        # If the username is not in the dictionary, then return false (prevents exceptions).
        if username not in users:
            return False
        # Else, if the username is in the dictionary, just
        # check whether the value is the same as the password enter.
        return users[username] == password
