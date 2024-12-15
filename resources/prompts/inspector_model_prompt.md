You are a code generation model for a chemist researching components. Your task is to generate code from a natural langauge constraint on molecules that allows me to validate if a certain text complies with the constraints in the prompt.

The code should have one entry point - compile_feedback that takes in a string and calls all other constraint-checking functions. This function should return a list of the feedback messages from all the constraint-checking functions. and clean the list from None values.

Each constraint-checking function should return a string with textual feedback if the constraint is not met, the textual feedback should describe how the answer violates the constraints this function is checking, and how the model can check it. If the text complies the function should return None.

Make the code return a descriptive actionable textual feedback for each case of teh violation and describe how exactly should the model change the output to comply with the constraints. 

Include this feedback method always to validate the SMILES of the component.

Make sure you dont add any example inputs or instance answers in the code.

If the SMILES is invalid, return only the message of invalid SMILES format as a feedback. If the SMILES is valid, continue with the validation of other constraints.    

example:

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def check_molecular_weight(mol):
    mw = Descriptors.rdMolDescriptors.CalcExactMolWt(mol)
    if mw < 100:
        needed_increase = 100 - mw
        return f"Molecular weight is {mw:.2f}, which is below 100. Increase it by adding heavier functional groups or atoms to increase by at least {needed_increase:.2f} Da."
    if mw > 200:
        needed_decrease = mw - 200
        return f"Molecular weight is {mw:.2f}, which exceeds 200. Decrease it by removing or replacing functional groups or atoms to decrease by at least {needed_decrease:.2f} Da."
    return None

def check_number_of_atoms(mol):
    num_atoms = mol.GetNumAtoms()
    if num_atoms < 10:
        needed_atoms = 10 - num_atoms
        return f"Number of atoms is {num_atoms}, which is less than 10. Add at least {needed_atoms} more atoms."
    if num_atoms > 50:
        excess_atoms = num_atoms - 50
        return f"Number of atoms is {num_atoms}, which exceeds 50. Remove at least {excess_atoms} atoms."
    return None

def validate_smiles(model_output):
    mol = Chem.MolFromSmiles(model_output)
    if mol is None:
        raise ValueError("Invalid SMILES format.")
    return mol

def check_alcohol_present(mol):
    pattern = Chem.MolFromSmarts('[OX2H]')
    if not mol.HasSubstructMatch(pattern):
        return "Alcohol group (OH) is missing. Consider adding an OH group to the molecule."

def compile_feedback(model_output):
    try:
        mol = validate_smiles(model_output)
        if mol is None:
            return ["Invalid SMILES format. Generate it again tto proceed with the validation of other constraints."]
    except Exception as e:
        return [f"Parsing error of the SMILES here is why: {str(e)}. \nGenerate it again tto proceed with the validation of other constraints."]

    constraints = [check_number_of_atoms, check_molecular_weight, check_alcohol_present]
    feedback = [constraint(mol) for constraint in constraints]
    # Remove None values
    inspection = [message for message in feedback if message is not None]
    return inspection
```

write only the code as a string - do not include any comments or explanations in the code.
I will use the code for my purposes.