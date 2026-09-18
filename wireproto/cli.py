import json, sys
from pathlib import Path
from .generator import generate
from .constraints import normalize
from .renderer import render_svg

def main():
    prompt = " ".join(sys.argv[1:]) or "dashboard com sidebar, cards, gráfico e tabela"
    graph = normalize(generate(prompt))
    out = Path("output"); out.mkdir(exist_ok=True)
    (out/"layout.json").write_text(json.dumps(graph.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    (out/"wireframe.svg").write_text(render_svg(graph), encoding="utf-8")
    print("Generated output/layout.json and output/wireframe.svg")

if __name__ == "__main__": main()
