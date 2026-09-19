from .schema import LayoutGraph

def _snap(value: int, grid: int) -> int:
    return round(value / grid) * grid

def normalize(graph: LayoutGraph, grid: int = 8) -> LayoutGraph:
    """Deterministically repair noisy vision geometry."""
    for n in graph.nodes:
        n.x = max(0, _snap(n.x, grid))
        n.y = max(0, _snap(n.y, grid))
        n.w = max(grid, _snap(n.w, grid))
        n.h = max(grid, _snap(n.h, grid))
        n.w = min(n.w, max(grid, graph.width-n.x))
        n.h = min(n.h, max(grid, graph.height-n.y))

    by_id = {n.id: n for n in graph.nodes}
    for rel in graph.relations:
        if not rel.source or not rel.target:
            continue
        a, b = by_id.get(rel.source), by_id.get(rel.target)
        if not a or not b:
            continue
        if rel.type == "equal-width" and abs(a.w-b.w) <= grid*2:
            width = _snap(round((a.w+b.w)/2), grid)
            a.w = min(width, graph.width-a.x)
            b.w = min(width, graph.width-b.x)
        elif rel.type == "equal-height" and abs(a.h-b.h) <= grid*2:
            height = _snap(round((a.h+b.h)/2), grid)
            a.h = min(height, graph.height-a.y)
            b.h = min(height, graph.height-b.y)

    for child in graph.nodes:
        parent = by_id.get(child.parent) if child.parent else None
        if not parent:
            continue
        child.x = max(parent.x, min(child.x, parent.x+parent.w-grid))
        child.y = max(parent.y, min(child.y, parent.y+parent.h-grid))
        child.w = max(grid, min(child.w, parent.x+parent.w-child.x))
        child.h = max(grid, min(child.h, parent.y+parent.h-child.y))
    return graph
