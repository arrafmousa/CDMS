from datasets import load_dataset

from extract_statistics import when_was_model_correct_vs_when_inspector_approve, open_files


def find_answer(inputs, ds):
    ds_desc, ds_smiles = ds['test']['description'], ds['test']['SMILES']
    for i_desc, i_smiles in zip(ds_desc, ds_smiles):
        if i_desc in inputs:
            return i_smiles


def infer_results(ds, collected_data_):
    results = []
    for data_sample in collected_data_:
        model_outputs = data_sample['icicle_outputs']
        correct_answer = find_answer(data_sample['input'], ds)
        results.append([correct_answer == o for o in model_outputs])
    return results


ds = load_dataset("liupf/ChEBI-20-MM")

collected_data = open_files("outputs/test_summary3114.jsonl")

validator_results = infer_results(ds, collected_data)
print(validator_results)
