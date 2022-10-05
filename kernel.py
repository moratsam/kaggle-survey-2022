from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class Dataset:
    id: int
    name: str
    url: str
    

@dataclass
class Kernel:
    id: int
    notebook_id:    int             # Needed to download the notebook.
    title:          str
    url:            str
    datasets:       List[Dataset]
    medal:          Optional[str]   # None/'Bronze' ..
    libs:           List[str]       # Libraries used by the notebook.
    keywords:       List[str]       # TODO 
    questions:      List[str]       # TODO
    topic:          str = ""        # TODO
    comments:       int = 0
    views:          int = 0
    votes:          int = 0
