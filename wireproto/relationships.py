"""Infer hierarchy and first-class spatial relationships."""
from .schema import Node, Relation

def _contains(a: Node, b: Node) -> bool:
    return a.x <= b.x and a.y <= b.y and a.x+a.w >= b.x+b.w and a.y+a.h >= b.y+b.h

def infer(nodes: list[Node], tolerance: int = 8) -> tuple[list[Node], list[Relation]]:
    by_id = {n.id: n for n in nodes}
    for child in nodes:
        if child.parent and child.parent in by_id:
            continue
        parents = [n for n in nodes if n.id != child.id and _contains(n, child)]
        if parents:
            child.parent = min(parents, key=lambda n: n.w*n.h).id

    for node in nodes:
        node.children = []
    for child in nodes:
        if child.parent in by_id:
            by_id[child.parent].children.append(child.id)

    relations: list[Relation] = []
    seen = set()
    def add(kind, source, target):
        key = (kind, source, target)
        if key not in seen:
            seen.add(key)
            relations.append(Relation(type=kind, source=source, target=target))

    for i, node in enumerate(nodes):
        for other in nodes[i+1:]:
            if abs((node.y+node.h/2)-(other.y+other.h/2)) <= tolerance:
                add("aligned-y", node.id, other.id)
            if abs(node.x-other.x) <= tolerance:
                add("aligned-left", node.id, other.id)
            if abs(node.w-other.w) <= tolerance:
                add("equal-width", node.id, other.id)
            if abs(node.h-other.h) <= tolerance:
                add("equal-height", node.id, other.id)
            if node.y+node.h <= other.y:
                add("above", node.id, other.id)
            elif other.y+other.h <= node.y:
                add("above", other.id, node.id)
            if node.x+node.w <= other.x:
                add("left-of", node.id, other.id)
            elif other.x+other.w <= node.x:
                add("left-of", other.id, node.id)
    return nodes, relations
