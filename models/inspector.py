import re


class Inspector:
    def __init__(self, code: str):
        try:
            regex = r"```python\n(.*?)\n```"
            match = re.search(regex, code, re.DOTALL)
            if match is None:
                self.code = code
            else:
                self.code = match.group(1)

            compile(self.code, "<string>", "exec")

        except SyntaxError as e:
            self.error = e
            # raise e

    def inspect(self, input_variable_name: str, input_value: str):
        get_result_code_line = f"\nresult = compile_feedback({input_variable_name})"
        clean_none = f"\nresult = [x for x in result if x is not None]"
        try:
            namespace = {input_variable_name: input_value}
            exec(self.code + get_result_code_line + clean_none, namespace)
            return namespace.get("result")
        except Exception as e:
            return [f"Error: {e}"]

    @staticmethod
    def convert_feedback_to_response(feedback: list[str]):
        requirement = '\n'.join([f'- {line}' for line in feedback])
        instructions = (
            # make list of string into bullets
            f"Your answer does not meet all the requirements in my request. "
            f"Here is a list of actions if you  follow will lead to better compliance with my request:\n"
            f"{requirement}"
            f"Please make the necessary changes and try again.\n"
            f"You MUST adhere to all the requirements in my request it is critical to my career.\n")

        return instructions
