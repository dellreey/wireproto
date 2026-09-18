from html import escape
from .schema import LayoutGraph

def render_svg(graph: LayoutGraph) -> str:
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{graph.width}" height="{graph.height}" viewBox="0 0 {graph.width} {graph.height}">', '<rect width="100%" height="100%" fill="white"/>']
    for n in graph.nodes:
        parts.append(f'<rect x="{n.x}" y="{n.y}" width="{n.w}" height="{n.h}" rx="8" fill="#f3f3f3" stroke="#555" stroke-width="2"/>')
        parts.append(f'<text x="{n.x+12}" y="{n.y+28}" font-family="Arial" font-size="16" fill="#333">{escape(n.label or n.type)}</text>')
    parts.append("</svg>")
    return "\n".join(parts)
