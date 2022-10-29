from datetime import datetime
from typing import Any, Dict, List, Optional

from dataclasses import dataclass

@dataclass
class Dataset:
    id: int
    name: str
    url: str
    

@dataclass
class Kernel:
    id: int
    notebook_id:        int             # Needed to download the notebook.
    title:              str
    created_at:         datetime        # Serialised as '%Y-%m-%d %H:%M:%S'.
    evaluation_date:    datetime        # Serialised as '%Y-%m-%d %H:%M:%S'.
    made_public_date:   datetime        # Serialised as '%Y-%m-%d %H:%M:%S'.
    year:               int             # Year when it was created.
    url:                str
    language:           str             # 'Python'/'R'.
    datasets:           List[Dataset]
    medal:              Optional[str]   # None/'Bronze' ..
    libs:               List[str]       # Libraries used by the notebook.
    keywords:           List[str]
    tags:               List[str]       # Pulled from meta kaggle.
    tier:               int             # Tier of the kernel's author [0-5].
    questions:          List[str]
    topic:              str = ""        # TODO
    comments:           int = 0
    views:              int = 0
    votes:              int = 0
