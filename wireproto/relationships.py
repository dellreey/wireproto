"""Infer spatial relationships and hierarchy."""
from .schema import Node

def _contains(a,b):
    return a.x<=b.x and a.y<=b.y and a.x+a.w>=b.x+b.w and a.y+a.h>=b.y+b.h

def infer(nodes: list[Node]) -> list[Node]:
    for child in nodes:
        parents=[n for n in nodes if n.id!=child.id and _contains(n,child)]
        if parents: child.parent=min(parents,key=lambda n:n.w*n.h).id
    for node in nodes:
        rel=[]
        for other in nodes:
            if node.id==other.id: continue
            if abs((node.y+node.h/2)-(other.y+other.h/2))<=8: rel.append(f"aligned-y:{other.id}")
            if abs(node.x-other.x)<=8: rel.append(f"aligned-left:{other.id}")
            if node.y+node.h<=other.y: rel.append(f"above:{other.id}")
            if node.x+node.w<=other.x: rel.append(f"left-of:{other.id}")
        node.relations=rel
    return nodes
