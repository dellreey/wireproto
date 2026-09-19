from .schema import LayoutGraph
from .extractor import extract
from .relationships import infer
from .constraints import normalize

def image_to_layout(detections: list[dict], width: int = 1440, height: int = 900) -> LayoutGraph:
    nodes = extract(detections)
    nodes, relations = infer(nodes)
    graph = LayoutGraph(width=width, height=height, nodes=nodes, relations=relations)
    return normalize(graph)
