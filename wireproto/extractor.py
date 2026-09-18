"""Structure extraction interface."""
from .schema import Node

def extract(detections: list[dict]) -> list[Node]:
    nodes=[]
    for i,d in enumerate(detections):
        x,y,w,h=map(int,d["bbox"])
        nodes.append(Node(id=d.get("id",f"node-{i}"),type=d.get("type","unknown"),x=x,y=y,w=w,h=h,label=d.get("label",d.get("type","unknown")),confidence=float(d.get("confidence",1.0))))
    return nodes
