from src.models import OpenAILLM, LLMModel
from src.actions import AnalyzeURL, ProcessCSV, SaveToFile, SendEmail, WriteText, SaveToVariable
import os

import json

from typing import List


class Planner:
    def __init__(self, llm_model: LLMModel):
        # note: instead this should be loading some yaml file with a configuration of the models
        default_prompt_path = os.path.join('data', 'default_system_queries', 'planner.txt')
        with open(default_prompt_path, 'r') as f:
            self.default_planner_prompt = f.read()
        self.llm = llm_model

    def validate_a_plan(self, plan: str):
        # mock
        return True

    def generate_a_plan(self, task: str):
        plan = self.llm.query_the_model(self.default_planner_prompt, task)
        while not self.validate_a_plan(plan):
            # here maybe ask the user for something.
            plan = self.llm.query_the_model(self.default_planner_prompt, task)

        plan_list = plan.split('\n')
        return plan_list


class ActionSelector:
    def __init__(self, llm_model: LLMModel):
        default_ag_path = os.path.join('data', 'default_system_queries', 'action_generator.txt')
        with open(default_ag_path, 'r') as f:
            self.default_ag_prompt = f.read()

        self.llm = llm_model

        functions_path = os.path.join('data', 'default_system_queries', 'functions.json')
        with open(functions_path, 'r') as f:
            self.functions = json.load(f)

    def parse_call(self, call):
        return call['name'], json.loads(call['arguments'])

    def generate_an_action(self, summary, descr: str):
        system_command = f'You are in the middle of realizing a task. A summary of previous results is: {summary} \n' \
                         f'Your next step in realizing the plan is: {descr}'
        user_command = 'Generate a one function call from available actions that realizes the next step using summary of previous results.'
        system_command = '\n'.join([self.default_ag_prompt, system_command])
        call = self.llm.query_the_model_for_call(system_command, user_command, self.functions)
        return self.parse_call(call)


class Summarizer:
    def __init__(self, llm_model: LLMModel):
        default_summarizer_path = os.path.join('data', 'default_system_queries', 'summarizer.txt')
        with open(default_summarizer_path, 'r') as f:
            self.default_summarizer_prompt = f.read()

        self.llm = llm_model

    def summarize(self, previous_summary: str, result: str, remaining_steps: List[str]):
        system_commend = self.default_summarizer_prompt
        remaining_steps_str = '[' + ';'.join(remaining_steps) + ']'
        user_command = f'previous summary: {previous_summary}\nresult: {result}\nremaining steps: {remaining_steps_str}\nCreate a new summary for the remaining steps.'
        new_summary = self.llm.query_the_model(system_commend, user_command)
        return new_summary


class MainLoop:
    def __init__(self, username: str):
        # instead this should be read from configuration
        self.model = "gpt-3.5-turbo"
        self.llm_model = OpenAILLM(self.model)

        self.username = username

        self.planner = Planner(self.llm_model)
        self.action_generator = ActionSelector(self.llm_model)
        self.summarizer = Summarizer(self.llm_model)

        self.summary = 'This is the first step. there is no summary at this point.'

        analyze_url = AnalyzeURL(username, self.llm_model)
        self.functions = {
            'analyze_url': analyze_url,
            'process_csv': ProcessCSV(username, self.llm_model, analyze_url),
            'save_to_file': SaveToFile(username),
            'send_email': SendEmail(username),
            'write_text': WriteText(username, self.llm_model),
            'save_to_variable': SaveToVariable(username)
        }

    def do_the_task(self, task: str):
        plan = self.planner.generate_a_plan(task)

        print('the plan to solve it is: ', plan)

        for i, plan_el in enumerate(plan):
            print('current element of the plan: ', plan_el)

            # generate an action
            args = self.functions['write_text'](self.summary, f'select only the parts that are absolutely necessary for {plan_el}')
            print('arguments: ', args)

            try:
                f, kwargs = self.action_generator.generate_an_action(args, plan_el)
                print('i am doing: ', f, ' with ', kwargs)
            except KeyError: # this should be in a different place and not handled by an exception, but by a verification
                # no function call from openai api
                print('NO FUNCTION CALL')
                continue

            # execute the action
            selected_action = self.functions[f]
            res = selected_action(**kwargs)

            # generate new summary
            self.summary = self.summarizer.summarize(self.summary, res, plan[i+1:])
            print('current summary: ', self.summary)

            # todo: add refinement of the plan and verification of the results
        return res

