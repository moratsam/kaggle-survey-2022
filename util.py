from kaggle_io.local import read_kernels
from kaggle_io.remote import objectivise_kernel, query_kernels

from typing import List

from kernel import Kernel

def get_kernels(from_disk: bool = False, fname: str = 'all_kernels.json') -> List[Kernel]:
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
