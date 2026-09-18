from .schema import LayoutGraph
from .extractor import extract
from .relationships import infer
from .constraints import normalize

def image_to_layout(detections: list[dict], width: int=1440, height: int=900) -> LayoutGraph:
    nodes=infer(extract(detections))
    return normalize(LayoutGraph(width=width,height=height,nodes=nodes))
