from kaggle_io.local import dump_kernels, read_kernels, read_notebook
from kaggle_io.remote import objectivise_kernel, query_kernels, download_notebook
from notebook_parser import NotebookParser

from typing import List

from kernel import Kernel

def parse_questions_and_dump():
    """
    Parse questions, dump updated kernels to disk.
    """
    kernels = get_kernels(from_disk=True)
    notebook_generator = generate_notebooks(kernels, from_disk=True)
    for i,notebook in enumerate(notebook_generator):
        kernels[i].questions = NotebookParser(notebook).parse_questions()
    dump_kernels(kernels) 

def generate_notebooks(kernels: List[Kernel] = [], from_disk = False):
    """
    Yield notebooks, one at a time. 
    This is done to prevent all notebooks from being simultaneously loaded in memory.
    """
    if not kernels:
        kernels = get_kernels(from_disk)
    for k in kernels:
        notebook = get_notebook(k.notebook_id, from_disk)
        yield notebook

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
