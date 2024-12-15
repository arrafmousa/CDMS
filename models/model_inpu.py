class ModelInput:
    def __init__(self, system_prompt: str, messages: list[str], few_shot: list[str]):
        self.system_prompt = {"role": "system", "content": system_prompt}
        self.few_shot = few_shot
        self.messages = messages

    def to_dict(self):
        parsed_messages = []
        roles = ["user", "assistant"]  # Alternating roles
        for i, text in enumerate(self.few_shot + self.messages):
            parsed_messages.append({"role": roles[i % 2], "content": text})

        return [self.system_prompt] + parsed_messages
