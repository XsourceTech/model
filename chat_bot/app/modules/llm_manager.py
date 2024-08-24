########### Libraries ###########
# standard imports
import json
from abc import ABC, abstractmethod
# installed imports
import tiktoken
import openai
# from mistralai.client import MistralClient
# from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
# from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
# from transformers import AutoTokenizer

from pathlib import Path
module_path = Path.cwd().parent
# internal imports
from config.settings import (
    OPENAI_API_KEY,
    # MISTRAL_BASE,
    # MISTRAL_KEY,
)


########### Class ###########
class LLMManger(ABC):
    """Class for using the GPT model for encoding and generation of text.

    Attributes:
        _llm_name (str): The name of the LLM model.
        _client: The client for the Azure API.
        _models_encoding_map (dict): The mapping of the models supported for encoding.
        _models_generation_map (dict): The mapping of the models supported for generation.
        TEMPERATURE (float): The temperature for the model.
    """

    def __init__(self, llm_name: str) -> None:
        """Initialise the LLMManger class."""
        self._llm_name = llm_name
        self._client = None
        self._models_generation_map = None
        self.TEMPERATURE = 0.1

    @property
    def llm_name(self) -> str:
        """Get the name of the LLM model."""
        return self._llm_name

    def _check_existence_model(self, model: str, models_mapping: list[str]) -> None:
        """Check if the model is supported by the GPT connector.

        Args:
            model: The name of the model to be checked.
            models_mapping: The mapping of the models supported for the task

        Raises:
            ValueError: If the model is not supported.
        """
        if model not in models_mapping:
            raise ValueError(f"Unsupported model: {model}")

    @abstractmethod
    def _get_tokens(
        self,
        text: str,
        model: str,
    ) -> list:
        """Get the tokens for a given text.

        Args
            text : text for calculation

        Returns:
            List of tokens
        """
        pass

    def count_tokens(self, model: str, text: str) -> int:
        """Count the the number of token for a given model

        Args
            text : text for calculation
            model : name of the model used for LLM

        Returns:
            Number of tokens
        """
        # check if the model is supported
        self._check_existence_model(
            model,
            list(self._models_encoding_map.keys())
            + list(self._models_generation_map.keys()),
        )

        # get the encoding for the model
        tokens = self._get_tokens(text, model)

        # calculate the number of tokens
        nb_tokens = len(tokens)

        return nb_tokens

    def _count_cost_embedding(self, model: str, text: str) -> float:
        """Calculate the cost of token usage based on the specified model of encoding.

        Args:
            model : name of the model used by openai
            text : text for encoding

        Returns:
            Cost of the token usage
        """
        # check if the model is supported
        self._check_existence_model(
            model, list(self._models_encoding_map.keys()))

        # count the number of tokens
        num_tokens = self.count_tokens(model, text)

        price_encoding = self._models_encoding_map[model]["price_encoding_by_token"]

        # calculate the cost of encoding
        cost_encoding = price_encoding * num_tokens

        return cost_encoding

    def _count_cost_generation(self, model: str, input: str, output: str) -> float:
        """Calculate the cost of token usage based on the specified model of generation.

        Args:
            model : name of the model used by openai.
            input : input text for generation.
            output : output text of the llm.

        Returns:
            Cost of the token usage.
        """
        # check if the model is supported
        self._check_existence_model(model, self._models_generation_map.keys())

        # count the number of tokens
        num_tokens_input = self.count_tokens(model, input)
        num_tokens_output = self.count_tokens(model, output)

        price_input = self._models_generation_map[model]["price_input_by_token"]
        price_output = self._models_generation_map[model]["price_output_by_token"]

        # calculate the cost of generation
        cost_input = price_input * num_tokens_input
        cost_output = price_output * num_tokens_output
        cost_total = cost_input + cost_output

        return cost_total

    @abstractmethod
    def _get_llm_response(
        self, user_message: str, system_message: str, model_generation: str
    ):
        """Get the response from the LLM model for a given message.

        Args:
            user_message: The message to get the response for.
            system_message: The system message to be used in the GPT model.
            model_generation: The model to be used for generation.

        Returns:
            The response from the LLM model.
        """
        pass

    def get_response(
        self,
        user_message_or_memories: str | list,
        system_message: str,
        model_generation: str,
        get_cost: bool = False,
    ) -> str | tuple[str, float]:
        """Get the response from the GPT model for a given message.

        Args:
            user_message: The user message or memories to get the response for.
            system_message: The system message to be used in the GPT model.
            model_generation: The model to be used for generation.
            get_cost: Whether to calculate the cost of the response.

        Returns:
            The response from the GPT model. If get_price is True, then the price is also returned.
        """
        # check if the model is supported
        self._check_existence_model(
            model_generation, self._models_generation_map.keys()
        )

        completion = self._get_llm_response(
            user_message_or_memories, system_message, model_generation
        )
        output = completion.choices[0].message.content

        # calculate the prices used for the response
        if get_cost:
            cost = self._count_cost_generation(
                model_generation,
                user_message_or_memories + " " + system_message,
                output,
            )

        return (output, cost) if get_cost else output


########### Classes ###########
class GPTManager(LLMManger):
    """Class for using the GPT model for encoding and generation of text.

    Attributes:
        _client (AzureOpenAI): The client for the Azure OpenAI API.
        _models_encoding_map (dict): The mapping of the models supported for encoding.
        _models_generation_map (dict): The mapping of the models supported for generation.
    """

    def __init__(self, llm_name: str = "GPT") -> None:
        """Initialise the GPTManager class."""
        super().__init__(llm_name)
        openai.api_key = OPENAI_API_KEY
        self._client = OpenAI()

        self._models_encoding_map = {
            "text-embedding-ada-002": {
                "model_name": "text-embedding-ada-002",
                "price_encoding_by_token": 1e-07,
            },
            "text-embedding-3-small": {
                "model_name": "text-embedding-3-small",
                "price_encoding_by_token": 2e-08,
            },
            "text-embedding-3-large": {
                "model_name": "text-embedding-3-large",
                "price_encoding_by_token": 13e-08,
            },
        }

        self._models_generation_map = {
            "gpt-4o-mini": {
                "model_name": "gpt-4o-mini-2024-07-18",
                "price_input_by_token": 15e-08,
                "price_output_by_token": 6e-07,
            },
            "gpt-4o": {
                "model_name": "gpt-4o-2024-05-13",
                "price_input_by_token": 5e-06,
                "price_output_by_token": 15e-06,
            },
            "gpt-4-turbo": {
                "model_name": "gpt-4-turbo-2024-04-09",
                "price_input_by_token": 1e-05,
                "price_output_by_token": 3e-05,
            },

        }

    def _get_tokens(
        self,
        text: str,
        model: str,
    ) -> list:
        """Get the tokens for a given text.

        Args:
            text : text for calculation
            model : name of the model used by openai

        Returns:
            tokens: List of tokens
        """
        # get the encoding for the model
        encoding = tiktoken.encoding_for_model(model)

        # calculate the number of tokens
        tokens = encoding.encode(text)

        return tokens

    def _get_llm_response(
        self,
        user_message_or_memories: str | list,
        system_message: str = "You are an assistant.",
        model_generation: str = "gpt-4o-mini",
    ):
        """Get the response from the LLM model for a given message.

        Args:
            user_message_or_memories: The user message or memories to get the response for.
            system_message: The system message to be used in the GPT model.
            model_generation: The model to be used for generation.

        Returns:
            The response from the LLM model.
        """
        messages_for_api = [{"role": "system", "content": system_message}]
        messages_for_api += user_message_or_memories if isinstance(
            user_message_or_memories, list) else [
            {"role": "user", "content": user_message_or_memories}
        ]

        completion = self._client.chat.completions.create(
            model=self._models_generation_map[model_generation]["model_name"],
            temperature=self.TEMPERATURE,
            messages=messages_for_api,
            n=1,
        )

        return completion

    def encode(
        self,
        text: str,
        model_embedding: str = "text-embedding-ada-002",
        get_cost: bool = False,
    ) -> dict[str, float]:
        """Get the embedding for a given text.

        Args:
            text: The text to get the embedding for.
            model: The model to be used for encoding.
            get_cost: Whether to calculate the cost of the response.

        Returns:
            The embedding for the given text. If get_price is True, then the price is also returned.
        """
        # check if the model is supported
        self._check_existence_model(
            model_embedding, list(self._models_encoding_map.keys())
        )
        try:
            response = self._client.embeddings.create(
                input=text,
                model=self._models_encoding_map[model_embedding]["model_name"],
            )

            # calculate the prices used for the response
            if get_cost:
                cost = self._count_cost_embedding(model_embedding, text)

            embeddings = response.data[0].embedding

            return (embeddings, cost) if get_cost else embeddings

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(text)
            raise


# class MistralManager(LLMManger):
#     """Class for using the Mistral model for generation of text.
#
#     Attributes:
#         _client (MistralClient): The client for the Mistral API.
#         _models_encoding_map (dict): The mapping of the models supported for encoding.
#         _models_generation_map (dict): The mapping of the models supported for generation.
#         _tokenizer (MistralTokenizer): The tokenizer for the Mistral model used for counting tokens.
#     """
#
#     def __init__(self, llm_name: str = "Mistral") -> None:
#         """Initialise the GPTManager class."""
#         super().__init__(llm_name)
#         self._client = MistralClient(
#             endpoint=MISTRAL_BASE, api_key=MISTRAL_KEY)
#
#         self._models_encoding_map = {}
#         self._models_generation_map = {
#             "mistral-large": {
#                 "model_name": "mistral-large",
#                 "price_input_by_token": 4e-06,
#                 "price_output_by_token": 12e-06,
#             },
#         }
#         self._tokenizer = None
#
#     def _get_tokens(self, text: str, model: str = None) -> list:
#         """Get the tokens for a given text.
#
#         Args:
#             text : text for calculation
#             model : name of the model used, but not used in this case with Mistral
#
#         Returns:
#             tokens: List of tokens
#         """
#         if not self._tokenizer:
#             self._tokenizer = AutoTokenizer.from_pretrained(
#                 "mistralai/Mistral-7B-v0.1")
#
#         # get the encoding for the model
#         tokens = self._tokenizer(
#             [text],
#             return_tensors="pt",
#         ).input_ids[0]
#
#         return tokens
#
#     def _get_llm_response(
#         self,
#         user_message_or_memories: str | list,
#         system_message: str = "You are an assistant.",
#         model_generation: str = "mistral-large",
#     ):
#         """Get the response from the LLM model for a given message.
#
#         Args:
#             user_message: The message to get the response for.
#             system_message: The system message to be used in the Mistral model.
#             model_generation: The model to be used for generation.
#
#         Returns:
#             The response from the LLM model.
#         """
#         completion = self._client.chat(
#             model=self._models_generation_map[model_generation]["model_name"],
#             messages=[
#                 ChatMessage(role="system", content=system_message),
#                 ChatMessage(role="user", content=user_message_or_memories),
#             ],
#             max_tokens=10000,
#             temperature=self.TEMPERATURE,
#         )
#
#         return completion
