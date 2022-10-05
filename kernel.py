from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Dataset:
    id: int
    name: str
    url: str
    

@dataclass_json
@dataclass
class Kernel:
    id: int
    notebook_id:    int            # Needed to download the notebook.
    title:          str
    url:            str
    datasets:       List[Dataset]
    medal:          Optional[str]    # None/'Bronze' ..
    libs:           List[str]       # Libraries used by the notebook.
    comments:       int = 0
    views:          int = 0
    votes:          int = 0

    # TODO
    """
    keywords:    List[str]
    questions:    List[int]
    topic:        Any = None
    """
