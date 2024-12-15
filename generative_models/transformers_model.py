from transformers import T5ForConditionalGeneration, T5Tokenizer

from generative_models.generative_model import GenerativeModel
import selfies as sf


class BioT5Plus(GenerativeModel):
    def __init__(self):
        self.model = T5ForConditionalGeneration.from_pretrained('QizhiPei/biot5-plus-base-chebi20')
        self.tokenizer = T5Tokenizer.from_pretrained("QizhiPei/biot5-plus-base-chebi20", model_max_length=512)

    def generate(self, message: str) -> str:
        task_definition = 'Definition: You are given a molecule description in English. Your job is to generate the molecule SELFIES that fits the description.\n\n'
        text_input = "the molecule is" + message
        task_input = f'Now complete the following example -\nInput: {text_input}\nOutput: '

        model_input = task_definition + task_input

        tokenized = self.tokenizer(model_input, return_tensors="pt", truncation=True, return_overflowing_tokens=True)
        if tokenized.get("overflowing_tokens").numel() > 0:
            print("Truncation occurred.")
            print("Overflowing tokens:", tokenized["overflowing_tokens"])

        input_ids = tokenized.input_ids

        generation_config = self.model.generation_config
        generation_config.max_length = 512
        generation_config.num_beams = 1

        outputs = self.model.generate(input_ids, generation_config=generation_config)
        output_selfies = self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace(' ', '')

        return sf.decoder(output_selfies)
