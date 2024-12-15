from generative_models.generative_model import GenerativeModel
import os
from openai import AzureOpenAI

from models.model_inpu import ModelInput


class AzureGenModel(GenerativeModel):

    def __init__(self, openai_key: str, api_version: str, azure_endpoint: str, deployment_name: str, max_tokens=150):
        self.client = AzureOpenAI(
            api_key=openai_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )

        self.max_tokens = max_tokens
        self.deployment_name = deployment_name

    def generate(self, model_input: ModelInput):
        return self.client.chat.completions.create(
            model=self.deployment_name,
            messages=model_input.to_dict(),
            max_tokens=self.max_tokens,
        ).choices[0].message.content
