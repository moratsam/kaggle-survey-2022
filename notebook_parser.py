from re import findall
from typing import Any, Dict, List, Optional


def sanitise(string: str) -> str:
    """
    Huge pain in the ass.
    Replace substrings from the input string with whitespaces.
    """
    REPLACE = [r'\n', r'\r', r'\t']
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
        def make_alpha(string: str) -> str:
            """
            Return only alphabetic characters from string.
            """
            return ''.join(char for char in string if char.isalpha())

        notebook = sanitise(notebook).split()
        imports = set()
        
        if language == 'Python':
            for i, word in enumerate(notebook):
                if make_alpha(word) == "import":
                    # Check for pattern "from X import Y"
                    if "from" in notebook[i-2]:
                        library = notebook[i-1]
                    # Check for pattern "import X"
                    else:
                        library = notebook[i+1]
                    # If library = 'X.Y.Z', take just 'X'.
                    library = library.split('.')[0]
                    imports.add(make_alpha(library))

        elif language == 'R':
            for word in notebook:
                if "library(" in word:
                    start_ix = word.index("library(") + len("library(")
                    end_ix = 0
                    for i, char in enumerate(f"{word[start_ix:]}."):
                        if not char.isalnum():
                            end_id=i
                            break
                    library = word[start_ix:end_ix]
                    # If library = 'X.Y.Z', take just 'X'.
                    library = word[8:-1].split('.')[0]
                    imports.add(make_alpha(library))

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
