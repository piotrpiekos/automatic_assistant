from src.models.LLMModel import LLMModel

import openai
import os


class OpenAILLM(LLMModel):
    def __init__(self, model_name: str):
        self.model_name = model_name
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def query_the_model(self, system_query: str, user_query: str):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_query},
                {"role": "user", "content": user_query}
            ]
        )

        # todo: add error handling
        response_text = response['choices'][0]['message']['content']
        return response_text

    def query_the_model_for_call(self, system_query, user_query, functions):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_query},
                {"role": "user", "content": user_query}
            ],
            functions=functions
        )
        # todo: add error handling
        return response["choices"][0]['message']['function_call']