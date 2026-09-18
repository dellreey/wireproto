from .schema import LayoutGraph, Node

def generate(prompt: str) -> LayoutGraph:
    p = prompt.lower()
    g = LayoutGraph()
    g.nodes.append(Node("header", "header", 24, 24, 1392, 72, label="Header"))
    if "sidebar" in p or "dashboard" in p:
        g.nodes.append(Node("sidebar", "sidebar", 24, 112, 240, 764, label="Navigation"))
        x, w = 288, 1128
    else:
        x, w = 24, 1392
    g.nodes.append(Node("title", "text", x, 120, w, 64, label="Page title"))
    card_w = (w - 48) // 3
    for i in range(3):
        g.nodes.append(Node(f"card-{i+1}", "card", x+i*(card_w+24), 208, card_w, 150, label=f"Metric {i+1}"))
    g.nodes.append(Node("main", "chart", x, 382, int(w*0.62), 300, label="Primary content"))
    g.nodes.append(Node("secondary", "panel", x+int(w*0.62)+24, 382, w-int(w*0.62)-24, 300, label="Secondary"))
    g.nodes.append(Node("table", "table", x, 706, w, 170, label="Data table"))
    return g
