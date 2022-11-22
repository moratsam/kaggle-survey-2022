from datetime import datetime
from typing import Any, Dict, List, Optional

from dataclasses import dataclass

@dataclass
class Dataset:
    id:   int   # Dataset id (taken from Kaggle).
    name: str   # Dataset name.
    url:  str   # Dataset url.
    

@dataclass
class Kernel:
    id: int                             # Kernel id (taken from Kaggle).
    notebook_id:        int             # Needed to download the notebook.
    title:              str             # Notebook title.
    created_at:         datetime        # Serialised as '%Y-%m-%d %H:%M:%S'.
    evaluation_date:    datetime        # Serialised as '%Y-%m-%d %H:%M:%S'.
    made_public_date:   datetime        # Serialised as '%Y-%m-%d %H:%M:%S'.
    year:               int             # Year when it was created.
    url:                str             # Notebook url.
    language:           str             # 'Python'/'R'.
    datasets:           List[Dataset]   # Datasets used by the notebook.
    medal:              Optional[str]   # None/'Bronze' ..
    libs:               List[str]       # Libraries used by the notebook.
    keywords:           List[str]       # Empty for now.
    tags:               List[str]       # Pulled from meta kaggle.
    tier:               Optional[str]   # Tier of the kernel's author.
    questions:          List[str]       # Questions mentioned in the notebook.
    topic:              str = ""        # Empty for now.
    comments:           int = 0         # Number of comments received by the notebook.
    views:              int = 0         # Number of views received by the notebook.
    votes:              int = 0         # Number of votes received by the notebook.
