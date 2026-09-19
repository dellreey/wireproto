from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class BBox:
    x: int
    y: int
    width: int
    height: int


@dataclass
class LayoutSpec:
    direction: Optional[str] = None
    gap: Optional[int] = None
    align: Optional[str] = None
    justify: Optional[str] = None


@dataclass
class Relation:
    type: str
    source: Optional[str] = None
    target: Optional[str] = None
    nodes: List[str] = field(default_factory=list)
    confidence: float = 1.0


@dataclass
class Node:
    id: str
    type: str
    bbox: BBox
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    label: str = ""
    text: str = ""
    confidence: float = 1.0
    layout: LayoutSpec = field(default_factory=LayoutSpec)
    constraints: Dict[str, Any] = field(default_factory=dict)
    visual_role: Optional[str] = None

    @property
    def x(self) -> int:
        return self.bbox.x

    @x.setter
    def x(self, value: int) -> None:
        self.bbox.x = value

    @property
    def y(self) -> int:
        return self.bbox.y

    @y.setter
    def y(self, value: int) -> None:
        self.bbox.y = value

    @property
    def w(self) -> int:
        return self.bbox.width

    @w.setter
    def w(self, value: int) -> None:
        self.bbox.width = value

    @property
    def h(self) -> int:
        return self.bbox.height

    @h.setter
    def h(self, value: int) -> None:
        self.bbox.height = value


@dataclass
class LayoutGraph:
    width: int = 1440
    height: int = 900
    nodes: List[Node] = field(default_factory=list)
    relations: List[Relation] = field(default_factory=list)

    def to_dict(self):
        return {
            "viewport": {"width": self.width, "height": self.height},
            "nodes": [asdict(n) for n in self.nodes],
            "relations": [asdict(r) for r in self.relations],
        }
