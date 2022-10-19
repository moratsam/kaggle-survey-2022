from re import findall
from typing import Any, Dict, List, Optional

class NotebookParser:
    def __init__(self, notebook: str):
        self.notebook = notebook

    def parse_libs(self) -> List[str]:
        """
        Given the raw notebook string, return list of all imported libraries.
        """
        notebook = self.notebook.split() # Split by whitespaces.
        imports = set()
        for i, word in enumerate(self.notebook):
            if '"import' == word:
                # If next word = 'X.Y.Z', take just 'X'.
                imports.add(self.notebook[i+1].split('.')[0])

        return list(imports)


    def parse_questions(self) -> List[str]:
        """
        Given the raw notebook string, return list of all substrings
        matching 'Q' followed by 1 or 2 digits.
        """
        questions = list(set(findall('Q\d{1,2}', self.notebook)))

        # Return sorted list.
        # When sorting, omit the first char (Q), to sort according to digits.
        return sorted(questions, key=lambda x: int(x[1:]))
