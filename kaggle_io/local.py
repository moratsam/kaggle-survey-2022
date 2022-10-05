import json
import os

from typing import Dict, List

from kernel import Kernel

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


def read_kernels(path: str) -> List[Kernel]:
    """
    Read kernels from a JSON file.
    """
    with open(path, 'r') as f:
        kernel_dicts = json.load(f)
        return [Kernel.from_json(k) for k in kernel_dicts] 

def dump_kernels(kernels: List[Kernel], fname: str = 'all_kernels.json'):
    """
    Dump kernels as JSON to disk.
    """
    kernel_dicts = [k.to_json() for k in kernels]
    with open(fname, 'w') as f:
        json.dump(kernel_dicts, f)


