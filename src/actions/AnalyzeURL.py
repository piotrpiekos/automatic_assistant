from src.actions.Action import ActionClass
from src.models import LLMModel

import requests
from bs4 import BeautifulSoup


class AnalyzeURL(ActionClass):
    def __init__(self, username: str, llm_model: LLMModel):
        super(AnalyzeURL, self).__init__(username)
        self.llm_model = llm_model

    def process_url_text(self, webtext: str, query: str):
        system_query = "You are a helpful web assistant that is summarizing the information about the website. " \
                       f"Users profile is described by {self.serialized_profile}. " \
                       f"Your goal is specified as: {query}. Find it in the text of the website provided by the user."
        user_query = webtext
        return self.llm_model.query_the_model(system_query, user_query)

    def log(self, link: str, query: str):
        return self.logtext(f'Investigating the link: \'{link}\' to look for \'{query}\'')

    def execute(self, link: str, query: str):
        r = requests.get(link, allow_redirects=True)
        soup = BeautifulSoup(r.content, "html.parser")
        webtext = soup.get_text()
        return self.process_url_text(webtext, query)
