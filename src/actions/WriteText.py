from src.actions import ActionClass
from src.models import LLMModel


class WriteText(ActionClass):
    def __init__(self, username: str, llm_model: LLMModel):
        super(WriteText, self).__init__(username)
        self.llm_model = llm_model

    def execute(self, original_text, purpose):
        system_query = 'You are a helpful assistant. Your goal is to select and rewrite the text that user gives with given purpose. ' \
                       f'The purpose of the text rewriting in this case is: {purpose}. Don\'t write anything apart from the rewritten text.'
        user_query = f"the original text is: {original_text}. Rewrite it with the following purpose in mind: {purpose}"
        return self.llm_model.query_the_model(system_query, user_query)
