import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from requests.sessions import Session
from typing import List

import pandas as pd

from kaggle_io.local import dump_kernels, read_kernels, dump_notebook, read_notebook
from kaggle_io.remote import objectivise_kernel, query_kernels, download_notebook
from kernel import Kernel
from notebook_parser import NotebookParser

def get_notebook(notebook_id: int, from_disk: bool = False, full_path=False) -> str:
    if from_disk:
        return read_notebook(notebook_id, full_path)
    else:
        return download_notebook(notebook_id)[0]

def pull_notebooks(kernels: List[Kernel]) -> None:
    extensions = {'Python': 'ipynb', 'R': 'Rmd', 'UNKNOWN': "unknown_format.txt"}
    session = Session()
    for i,k in enumerate(kernels):
        if i < 1586:
            continue
        print(f'Pulling {i}/{len(kernels)}')
        notebook, lang = download_notebook(session, k.notebook_id, k.language)
        if lang != k.language:
            print(f'Changing {k.id} lang: {k.language} --> {lang}')
            kernels[i].language = lang
            dump_kernels(kernels, path='tmp_all_kernels.csv')
        ext = extensions[lang]
        dump_notebook(notebook, f'{k.notebook_id}.{ext}')

    dump_kernels(kernels, path='tmp_all_kernels.csv')



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
    print(notebook_id)
    notebook = get_notebook(notebook_id, from_disk=True)
    parser = NotebookParser()
    questions = parser.parse_questions(notebook)
    libs = parser.parse_libs(notebook, language)
    return libs, questions


def parse_meta_kaggle_data():
    """ Files are from the meta kaggle dataset. """
    ks = get_kernels(from_disk=True)
    kernels = pd.read_csv('Kernels.csv')
    for i,k in enumerate(ks):
       try:
           ks[i].created_at = datetime.strptime(kernels.loc[kernels['Id'] == k.id]['CreationDate'].values[0], '%m/%d/%Y %H:%M:%S')
       except:
          pass
       ks[i].year = datetime.strftime(k.created_at, '%Y')
       try:
           ks[i].evaluation_date = datetime.strptime(kernels.loc[kernels['Id'] == k.id]['EvaluationDate'].values[0], '%m/%d/%Y')
       except:
          pass
       try:
           ks[i].made_public_date = datetime.strptime(kernels.loc[kernels['Id'] == k.id]['MadePublicDate'].values[0], '%m/%d/%Y')
       except:
          pass

    tags = pd.read_csv('Tags.csv')
    kernel_tags = pd.read_csv('KernelTags.csv')
    for i,k in enumerate(ks):
        tag_ids = kernel_tags.loc[kernel_tags['KernelId'] == k.id]['TagId'].values
        tag_names = tags.loc[tags['Id'].isin(tag_ids)]['Name'].values.tolist()
        ks[i].tags = tag_names

    users = pd.read_csv('Users.csv')
    for i,k in enumerate(ks):
        try:
            user_id = kernels.loc[kernels['Id'] == k.id, 'AuthorUserId'].values[0]
            tier = users.loc[users['Id'] == user_id, 'PerformanceTier'].values[0]
        except:
            tier = None
        ks[i].tier = tier

    dump_kernels(ks)



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
