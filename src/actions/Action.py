import json
import os


class ActionClass:
    def __init__(self, name):
        self.profile = None

        self.__load_profile(name)

        self.logtext = print

    def __load_profile(self, name):
        path = os.path.join('data', 'profiles', f'{name}.json')
        with open(path, 'r') as f:
            self.profile = json.load(f)

    def log(self, *args, **kwargs):
        return self.__class__

    def execute(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        self.log(*args, **kwargs)
        return self.execute(*args, **kwargs)

    @property
    def serialized_profile(self):
        return json.dumps(self.profile)
