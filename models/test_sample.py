import pubchempy as pcp

class TestSample:
    answer: dict
    test_input: str
    # smiles_answer:str

    golden_inspector_codes: list[str]

    def __init__(self, raw_sample: dict):
        self.answer = raw_sample["compound_data"]
        test_input = "Please generate a SMILES formula for a chemical compound that has all of the following properties:\n"
        golden_inspector_codes = []
        for prop in raw_sample["requirements"]:
            test_input += f"- {prop['nl_requirement']}\n"
            golden_inspector_codes.append(prop["code"])

        self.test_input = test_input
        self.golden_inspector_codes = golden_inspector_codes


