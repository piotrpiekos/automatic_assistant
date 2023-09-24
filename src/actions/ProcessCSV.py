from src.actions import ActionClass, AnalyzeURL
from src.models import LLMModel

import pandas as pd

from typing import List


class ProcessCSV(ActionClass):
    def __init__(self, username: str, llm_model: LLMModel, analyze_url: AnalyzeURL):
        super(ProcessCSV, self).__init__(username)
        self.llm_model = llm_model
        self.analyze_url = analyze_url
        # it would be better to not include other actions here and let it all be handled by the planner

    def generate_pandas_code(self, columns: List[str], task: str):
        system_query = "You are a helpful web assistant that produces the code in pandas to achieve result desired by the user. " \
                       f"Users profile is described by {self.serialized_profile}. " \
                       f"The pandas dataframe has columns: [{','.join(columns)}]. Write the code in python to execute " \
                       f"command provided by the user. Assume that pandas is already imported and the dataframe is " \
                       f"already loaded to a variable named df before execution of your code. " \
                       "Apart from the standard pandas api you can also use method self.analyze_url(link:str, query: str), " \
                       "that enters the website from the link and searches for elements specified by natural language in the query." \
                       "Write a code to achieve the user's query. Don't write anything else than a python code. " \
                       "At the end write user's end text result in the variable \'res\'. Make sure to save the result in the variable res"

        user_query = task
        return self.llm_model.query_the_model(system_query, user_query)

    def log(self, path_to_file: str, task: str):
        return self.logtext(f'Processing the file: \'{path_to_file}\' with the goal of \'{task}\'')

    def execute(self, path_to_file: str, task: str):
        df = pd.read_csv(path_to_file)
        code = self.generate_pandas_code(df.columns, task)
        print('code:\n', code)
        loc = {'df': df, 'self': self}

        # todo: validate whether compiles, and does what's required, perhaps with another call to LLM
        exec(code, globals(), loc)
        return loc['res']

