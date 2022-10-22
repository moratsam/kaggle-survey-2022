from re import findall
from typing import Any, Dict, List, Optional


def sanitise(string: str) -> str:
    """
    Huge pain in the ass.
    Replace substrings from the input string with whitespaces.
    """
    REPLACE = ['\\n', '\\r', '\n', '\r' '\t', '*', ',', '"', "'", ':', '-']
    string = f"---{string}---" # Add some buffer chars to each side.
    i = 0
    filtered_string = ""
    while i < len(string):
        match_found = False
        for r in REPLACE:
            if string[i:i+len(r)] == r:
                i += len(r)
                match_found = True
                break
        if match_found:
            filtered_string += " "
        else:
            filtered_string += string[i]
            i += 1
    return filtered_string
                

class NotebookParser:
    def parse_libs(self, notebook: str, language: str) -> List[str]:
        """
        Given the raw notebook string, return list of all imported libraries.
        """
        notebook = sanitise(notebook).split()
        imports = set()
        
        if language == 'Python':
            for i, word in enumerate(notebook):
                if word == "import":
                    # Check for pattern "from X import Y"
                    if "from" in notebook[i-2]:
                        library = notebook[i-1]
                    # Check for pattern "import X"
                    else:
                        library = notebook[i+1]
                    # If library = 'X.Y.Z', take just 'X'.
                    library = library.split('.')[0]
                    imports.add(library)

        elif language == 'R':
            for word in notebook:
                if word.startswith('library(') and word.endswith(')'):
                    # If library = 'X.Y.Z', take just 'X'.
                    library = word[8:-1].split('.')[0]
                    imports.add(library)

        return sorted(list(imports))


    def parse_questions(self, notebook: str) -> List[str]:
        """
        Given the raw notebook string, return list of all substrings
        matching 'Q' followed by 1 or 2 digits.
        """
        questions = list(set(findall('Q\d{1,2}', notebook)))

        # Return sorted list.
        # When sorting, omit the first char (Q), to sort according to digits.
        return sorted(questions, key=lambda x: int(x[1:]))
