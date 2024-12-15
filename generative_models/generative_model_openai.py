from generative_models.generative_model import GenerativeModel
from openai import OpenAI

from models.model_inpu import ModelInput


class GenerativeModelOpenai(GenerativeModel):
    def __init__(self, openai_key: str, api_version: str, endpoint: str, deployment_name: str, max_tokens=150):
        self.client = OpenAI(
            base_url =endpoint,
            api_key=openai_key,
        )

        self.deployment_name = deployment_name

    def generate(self, model_input: ModelInput):
        return self.client.chat.completions.create(
            model=self.deployment_name,
            messages=model_input.to_dict(),
            max_tokens=1000,
        ).choices[0].message.content

