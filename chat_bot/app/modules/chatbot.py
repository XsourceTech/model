########### Libraries ###########
# internal imports
from app.modules.llm_manager import GPTManager
from app.modules.prompt_template import Prompt

########### Class ###########


class Chatbot:
    def __init__(self):
        self._gpt_manager = GPTManager()
        self._prompt_manager = Prompt()
        self._memories = []

    def get_memory(self):
        return self._memories

    def set_memory(self, msg: str):
        self._memories.append({"role": "assistant", "content": msg})

    def generate_response_for_general_information(self, user_message: str) -> str:

        # update history with user message
        self._memories.append({"role": "user", "content": user_message})

        # get the system prompt
        system_message = self._prompt_manager.get_general_information_initialisation_system_prompt()

        # get the response from the GPT model
        response = self._gpt_manager.get_response(
            self._memories, system_message, model_generation="gpt-4o-mini")

        # update history with system message
        self._memories.append({"role": "assistant", "content": response})

        return response


    def summarize_general_information(self) -> str:
        # get the system prompt
        system_message = self._prompt_manager.get_summarize_general_information_system_prompt()

        # get the response from the GPT model
        response = self._gpt_manager.get_response(
            self._memories, system_message, model_generation="gpt-4o-mini")

        # update history with system message
        self._memories.append({"role": "assistant", "content": response})

        return response

    def generate_response_for_abstract(self, mft, user_message: str) -> str:
        self._memories.append({"role": "user", "content": user_message})
        self._memories.append({"role": "assistant", "content": mft})

        # get the system prompt
        system_message = self._prompt_manager.get_abstract_information_initialisation_system_prompt(mft=mft)

        # get the response from the GPT model
        response = self._gpt_manager.get_response(
            self._memories, system_message, model_generation="gpt-4o-mini")

        # update history with system message
        self._memories.append({"role": "assistant", "content": response})

        return response

    def summarize_abstract_information(self) -> str:
        # get the system prompt
        system_message = self._prompt_manager.get_summarize_abstract_information_system_prompt()

        # get the response from the GPT model
        response = self._gpt_manager.get_response(
            self._memories, system_message, model_generation="gpt-4o-mini")

        # update history with system message
        self._memories.append({"role": "assistant", "content": response})

        return response
