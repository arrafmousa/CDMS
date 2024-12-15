# Project Title

This project involves generating SMILES formulas for chemical compounds based on natural language requirements. It uses various models and datasets to validate the generated outputs.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://anonymous.4open.science/r/CDMS-C08D/
    ```
2. Navigate to the project directory:
    ```sh
    cd CDMS-C08D
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Prepare your test samples in a JSONL file and place it in the `resources/datasets` directory.
2. Run the simulation:
    ```sh
    python run_simulation.py
    ```

## Files

- `models/retriever.py`: Contains the `SearchableRequirements` class for searching and retrieving requirements and SMILES.
- `models/test_sample.py`: Contains the `TestSample` class for handling test samples.
- `experiments/20chi-sumary.py`: Script for extracting statistics and validating model outputs.
- `run_simulation.py`: Main script to run the simulation and validate the generated SMILES formulas.
- `TextGen` and `StructuredGen` directories: Contain `.dill` datasets that include recursive inspectors per hierarchical level. These datasets are to be loaded using the `dill` library as they are unshippable in text format.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
