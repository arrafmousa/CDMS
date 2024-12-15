from abc import ABC

from models.model_inpu import ModelInput


class GenerativeModel(ABC):

    def generate(self, messages: ModelInput):
        raise NotImplementedError("generate() method not implemented")