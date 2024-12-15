import json
import random
import re
from pathlib import Path
import rdkit
from datasets import load_dataset
from rdkit import Chem
from tqdm import tqdm

from generative_models.azure_gen_model import AzureGenModel
from generative_models.generative_model import GenerativeModel
from generative_models.generative_model_openai import GenerativeModelOpenai
from models.inspector import Inspector
from models.model_inpu import ModelInput
import os

from models.test_sample import TestSample

num_iter = 10

def run_single(model_inputs: ModelInput, inspector: Inspector, generative_model: GenerativeModel) -> (list[str], bool):
    generated_answers = []
    inspect_result = [None]

    progress_bar = tqdm(total=num_iter, desc="Processing")

    while len(inspect_result) > 0:
        # Generate a response
        try:
            generation_attempt = generative_model.generate(model_inputs)
            generated_answers.append(generation_attempt)
        except Exception as e:
            raise e

        # Inspect the response TODO: uncommetn this if running CoT
        # pattern = r"<Mol>(.*?)</Mol>"
        #
        # # Search for the pattern
        # match = re.search(pattern, generation_attempt)
        # if match is None:
        #     inspect_result = [
        #         "You did not conform to the expected output format. At the end please wite your answer wrapped by <Mol>(.*?)</Mol>"]
        # else:
        #     answer = match.group(1).replace(" ", "")
        #     inspect_result = inspector.inspect("answer", answer)

        # If the response is correct, return it
        if len(inspect_result) == 0:
            return generated_answers, True

        # If the response is incorrect, provide feedback
        inspector_feedback = inspector.convert_feedback_to_response(inspect_result)

        # Update the model input with the feedback
        model_inputs.messages.append(generated_answers[-1])
        model_inputs.messages.append(inspector_feedback)

        # If the expected output is reached, return the generated answers
        if len(generated_answers) >= num_iter:
            return generated_answers, False

        tqdm.update(progress_bar, 1)


def validate_answer(icicle_final_answer: str, golden_code_inspectors: list[str]):
    results = []
    for golden_code_inspector in golden_code_inspectors:
        try:
            ns = {"smiles": icicle_final_answer}
            exec(golden_code_inspector, ns)
            results.append(ns["result"])
        except Exception as e:
            results.append(False)
    return all(results)


def run_tests(inputs: list[TestSample]):
    openai_key = os.getenv("INSPECTOR_OPENAI_API_KEY")
    endpoint = os.getenv("INSPECTOR_OPENAI_API_BASE")
    deployment_name = "gpt-4o"
    api_version = "2024-02-01"

    with open("resources/inspector_model_prompt.md", "r") as f:
        inspector_model_prompt = f.read()

    with open("resources/generative_model_prompt.md", "r") as f:
        generative_model_prompt = f.read()

    coder_model = AzureGenModel(
        openai_key=openai_key,
        api_version=api_version,
        azure_endpoint=endpoint,
        deployment_name=deployment_name,
        max_tokens=1000,
    )

    openai_key = os.getenv("GENERATIVE_OPENAI_API_KEY")
    endpoint = os.getenv("GENERATIVE_OPENAI_API_BASE")
    deployment_name = "meta/llama-3.3-70b-instruct"
    api_version = "2024-02-01"

    generative_model = GenerativeModelOpenai(
        openai_key=openai_key,
        api_version=api_version,
        endpoint=endpoint,
        deployment_name=deployment_name,
        max_tokens=1000,
    )

    with open("resources/inspector_few_shots.json", "r", encoding='utf-8') as f:
        inspector_few_shots = json.load(f)

    with open("resources/generative_model_CoT_few_shots.json", "r", encoding='utf-8') as f:
        generative_few_shots = json.load(f)

    with open(f"outputs/test_summary_llama33-70b_CoT.jsonl", "w", encoding='utf-8') as f:
        for i, test_sample in tqdm(enumerate(inputs[:50])):
            coder_model_inputs = ModelInput(
                system_prompt=inspector_model_prompt,
                messages=[test_sample.test_input],
                few_shot=inspector_few_shots
            )

            generative_model_inputs = ModelInput(
                system_prompt=generative_model_prompt,
                messages=[test_sample.test_input],
                few_shot=generative_few_shots
            )

            inspector_code = coder_model.generate(
                model_input=coder_model_inputs,
            )

            inspector = Inspector(inspector_code)

            try:
                icicle_outputs, icicle_approved_answers = run_single(
                    model_inputs=generative_model_inputs,
                    generative_model=generative_model,
                    inspector=inspector,
                )
                icicle_final_answer = icicle_outputs[-1]
                answer_correct = validate_answer(icicle_final_answer, test_sample.golden_inspector_codes)
                test_summary = {
                    "input": test_sample.test_input,
                    "icicle_outputs": icicle_outputs,
                    "icicle_approved_answers": icicle_approved_answers,
                    "icicle_final_answer": icicle_final_answer,
                    "answer_correct": answer_correct,
                    "inspector_code": inspector.code,
                }

            except Exception as e:
                answer_correct = f"Error - {e}"
                test_summary = {
                    "input": test_sample.test_input,
                    "correct_answer": "icicle_final_answer",
                    "icicle_outputs": str(e),
                    "icicle_approved_answers": None,
                    "icicle_final_answer": None,
                    "answer_correct": False,
                    "inspector_code": inspector.code,
                }

            f.write(str(test_summary) + "\n")
            f.flush()

            color = "\033[32m" if answer_correct else "\033[31m"  # Green for True, Red for False
            reset = "\033[0m"

            print(f"{color}Test {i + 1}: {answer_correct} - \t Done {i + 1}/{len(inputs)}{reset}")


def load_test_files(path: Path) -> list[TestSample]:
    with open(path, "r") as f:
        inputs = f.readlines()
    test_set = []
    for raw_test_input in inputs:
        sample = json.loads(raw_test_input)
        test_set.append(TestSample(sample))

    random.shuffle(test_set)
    return test_set


if __name__ == "__main__":
    test_samples = load_test_files(Path("../CDMS/resources/datasets/chemGen.jsonl"))
    run_tests(test_samples)
