import csv
import json
import os
from ast import literal_eval
from datetime import datetime
from typing import Dict, List, Union


from kernel import Dataset, Kernel
from dataclass_csv import DataclassWriter, dateformat

PATH_NOTEBOOKS_DIR = os.environ.get('PATH_NOTEBOOKS_DIR') or "notebooks"


def dump_notebook(notebook: str, fname: str, full_path=False) -> None:
    """
    Dump a notebook to disk.
    If full_path=True, <fname> will be treated as a full path
        i.e. directory1/director2/notebook_filename.extension
    else:
        It will be dumped to the directory <PATH_NOTEBOOKS_DIR>
    """
    if full_path:
        path = full_path
    else:
        path = f"{PATH_NOTEBOOKS_DIR}/{fname}"
        # Check that the directory exists, else create it.
        if not os.path.isdir(PATH_NOTEBOOKS_DIR):
            os.mkdir(PATH_NOTEBOOKS_DIR)

    with open(path, 'w') as f:
        f.write(notebook)


def read_notebook(file_prefix: Union[int, str], full_path=False) -> str:
    """
    Read notebook from the PATH_NOTEBOOKS_DIR.
    file_prefix: Can be notebook_id (107352619) or filename (107352619.ipynb)
    """
    path = ""
    file_prefix = str(file_prefix)
    if full_path:
        path = file_prefix
    else:
        for fname in os.listdir(PATH_NOTEBOOKS_DIR):
            if fname.startswith(file_prefix):
                path = f"{PATH_NOTEBOOKS_DIR}/{fname}"
    
    if path == "":
        raise ValueError(f"File not found: {file_prefix}")
    
    with open(path, 'r') as f:
        return f.read()


def read_kernels(path: str = 'all_kernels.csv') -> List[Kernel]:
    """
    Read kernels from a CSV file.
    """
    data = list(csv.reader(open(path)))
    keys = data[0]
    kernels = [Kernel(**{k:v for k,v in zip(keys,row)}) for row in data[1:]]
    # csv.reader reads ints as strings, so they need to be transformed back to int.
    # Retarded, but it works.
    for k in kernels:
        for attr in ("id", "notebook_id", "comments", "views", "votes", "year"):
            setattr(k, attr, int(getattr(k, attr)))

        k.evaluation_date = datetime.strptime(k.evaluation_date, '%Y-%m-%d %H:%M:%S')
        k.created_at = datetime.strptime(k.created_at, '%Y-%m-%d %H:%M:%S')
        k.made_public_date = datetime.strptime(k.made_public_date, '%Y-%m-%d %H:%M:%S')

        # Transform string of list into list.
        k.questions = json.loads(k.questions.replace("'", '"'))
        k.libs = json.loads(k.libs.replace("'", '"'))

        # Transform string of list of Datasets into a list of Datasets.
        k.datasets = [Dataset(*tup) for tup in literal_eval(k.datasets)]

    return kernels


@dateformat('%Y-%m-%d %H:%M:%S')
def dump_kernels(kernels: List[Kernel], path: str = 'all_kernels.csv'):
    """
    Dump kernels as CSV to disk.
    """
    with open(path, 'w') as f:
        w = DataclassWriter(f, kernels, Kernel)
        w.write()
