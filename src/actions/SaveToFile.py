from src.actions import ActionClass


class SaveToFile(ActionClass):
    def __init__(self, username: str):
        super(SaveToFile, self).__init__(username)

    def log(self, text: str, path: str):
        self.logtext('Saving to file ', path)

    def execute(self, text: str, path: str):
        with open(path, 'w') as f:
            f.write(text)
