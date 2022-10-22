import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List

from kaggle_io.local import dump_kernels, read_kernels, read_notebook
from kaggle_io.remote import objectivise_kernel, query_kernels, download_notebook
from kernel import Kernel
from notebook_parser import NotebookParser

def get_notebook(notebook_id: int, from_disk: bool = False, full_path=False) -> str:
    if from_disk:
        return read_notebook(notebook_id, full_path)
    else:
        return download_notebook(notebook_id)


def get_kernels(from_disk: bool = False, fname: str = 'all_kernels.csv') -> List[Kernel]:
    """
    Return a list of all kernels.
    If from_disk = True, read them from a file named <fname>.
    Else, download them.
    """
    if from_disk:
        return read_kernels(fname)
    else:
        print("WARNING: will not download notebook-related data.")
        kernel_dicts = query_kernels()
        kernels = [objectivise_kernel(k) for k in kernel_dicts]
        return kernels


def notebook_yielder(kernels: List[Kernel] = [], from_disk = False):
    """
    Yield notebooks, one at a time. 
    This is done to prevent all notebooks from being simultaneously loaded in memory.
    """
    if not kernels:
        kernels = get_kernels(from_disk)
    for k in kernels:
        notebook = get_notebook(k.notebook_id, from_disk)
        yield notebook


def parse_notebook(notebook_id: int, language: str):
    """
    Parse libs & questions from a single notebook.
    """
    notebook = get_notebook(notebook_id, from_disk=True)
    parser = NotebookParser()
    questions = parser.parse_questions(notebook)
    libs = parser.parse_libs(notebook, language)
    return libs, questions


def parse_notebooks():
    """
    Parse libs and questions, dump updated kernels to disk.
    To speed things up, use multiprocessing (Note: Can't be run interactively).
    """
    kernels = get_kernels(from_disk=True)
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        future_to_kernel_ix = {executor.submit(parse_notebook, k.notebook_id, k.language): ix for ix,k in enumerate(kernels)}
        for future in as_completed(future_to_kernel_ix):
            libs, questions = future.result()
            ix = future_to_kernel_ix[future]
            kernels[ix].libs = libs
            kernels[ix].questions = questions

    dump_kernels(kernels)
