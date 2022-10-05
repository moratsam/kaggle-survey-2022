import csv
import json
import os

from typing import Dict, List

from kernel import Kernel
from dataclass_csv import DataclassWriter

PATH_NOTEBOOKS_DIR = "notebooks"


def dump_notebook(notebook: str, fname: str, full_path=False):
    """
    Dump a notebook to disk.
    If full_path=True, <fname> will be treated as a full path
        i.e. directory1/director2/notebook_filename.extension
    else:
        It will be dumped to the directory <PATH_NOTEBOOKS_DIR>
        with the extension "txt".
    """
    if full_path:
        path = full_path
    else:
        path = f"{PATH_NOTEBOOKS_DIR}/{fname}.txt"
        # Check that the directory exists, else create it.
        if not os.path.isdir(PATH_NOTEBOOKS_DIR):
            os.mkdir(PATH_NOTEBOOKS_DIR)

    with open(path, 'w') as f:
        f.write(notebook)


def read_kernels(path: str = 'all_kernels.csv') -> List[Kernel]:
    """
    Read kernels from a CSV file.
    """
    data = list(csv.reader(open(path)))
    keys = data[0]
    return [Kernel(**{k:v for k,v in zip(keys,row)}) for row in data[1:]]


def dump_kernels(kernels: List[Kernel], fname: str = 'all_kernels.csv'):
    """
    Dump kernels as CSV to disk.
    """
    with open(fname, 'w') as f:
        w = DataclassWriter(f, kernels, Kernel)
        w.write()
