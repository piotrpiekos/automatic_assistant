class LLMModel:
    def query_the_model(self, system_query: str, user_query: str):
        raise NotImplementedError

    def query_the_model_for_call(self, system_query, user_query, functions):
        raise NotImplementedError
