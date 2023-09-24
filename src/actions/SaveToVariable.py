"""
This is a mock, because chatgpt really wants to save results to variables
"""

from src.actions import ActionClass


class SaveToVariable(ActionClass):
    def __init__(self, username: str):
        super(SaveToVariable, self).__init__(username)

    def execute(self, data, variable_name):
        pass