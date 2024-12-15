import json
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import numpy as np
import pubchempy as pcp

class SearchableRequirements:
    def __init__(self, json_list):
        """
        Initialize the class with a list of JSON objects.

        Args:
            json_list (list): A list of JSON objects,
                              each containing "nl_requirement" and "compound_data" fields.
        """
        self.raw_data = json_list
        self.searchable_texts = []
        self.tokenized_corpus = []
        self.cid_to_smiles = {}

        # Prepare the searchable fields and additional data
        for idx, entry in enumerate(self.raw_data):
            print(idx)
            # Concatenate "nl_requirement" values to create searchable text
            nl_text = ''.join([d['nl_requirement'] for d in entry["requirements"]])
            self.searchable_texts.append(nl_text)

            # Tokenize for BM25
            self.tokenized_corpus.append(word_tokenize(nl_text.lower()))

            # Map CID to SMILES
            compound_data = entry.get("compound_data", {})
            cid = compound_data.get("cid")
            smiles = pcp.Compound.from_cid(cid).isomeric_smiles if cid else None
            if cid and smiles:
                self.cid_to_smiles[cid] = smiles

        print("to bm25")
        # Initialize BM25 for search
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def search_and_retrieve(self, query):
        """
        Search for the most relevant entry based on the query and retrieve its requirements and SMILES.

        Args:
            query (str): The search query.

        Returns:
            tuple: A tuple containing the list of "nl_requirement" and the SMILES string, or None if no match.
        """
        # Tokenize the query
        tokenized_query = word_tokenize(query.lower())

        # Get BM25 scores
        scores = self.bm25.get_scores(tokenized_query)

        # Find the best match
        best_index = np.argmax(scores)  # Use argmax to find the index of the highest score
        best_entry = self.raw_data[best_index]

        # Retrieve requirements and SMILES
        requirements = ''.join([d["nl_requirement"] for d in best_entry["requirements"]])
        compound_data = best_entry.get("compound_data", {})
        smiles = self.cid_to_smiles[compound_data["cid"]]

        if requirements and smiles:
            return ["the molecule must have the following"+'\n'.join(requirements), smiles]
        else:
            return None