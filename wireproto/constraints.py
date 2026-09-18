from .schema import LayoutGraph

def normalize(graph: LayoutGraph, grid: int = 8) -> LayoutGraph:
    for n in graph.nodes:
        n.x = max(0, round(n.x / grid) * grid)
        n.y = max(0, round(n.y / grid) * grid)
        n.w = max(grid, round(n.w / grid) * grid)
        n.h = max(grid, round(n.h / grid) * grid)
        n.w = min(n.w, graph.width - n.x)
        n.h = min(n.h, graph.height - n.y)
    return graph
