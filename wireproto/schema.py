from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class Node:
    id: str
    type: str
    x: int
    y: int
    w: int
    h: int
    parent: Optional[str] = None
    label: str = ""
    confidence: float = 1.0
    relations: List[str] = field(default_factory=list)

@dataclass
class LayoutGraph:
    width: int = 1440
    height: int = 900
    nodes: List[Node] = field(default_factory=list)

    def to_dict(self):
        return {"width":self.width,"height":self.height,"nodes":[asdict(n) for n in self.nodes]}
