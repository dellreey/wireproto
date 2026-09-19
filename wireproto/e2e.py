import argparse
import json
from pathlib import Path

from .pipeline import image_to_layout
from .renderer import render_svg
from .vision import extract_with_florence, load_json


def overlay_svg(graph, image_name: str) -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{graph.width}" height="{graph.height}">',
        f'<image href="{image_name}" width="{graph.width}" height="{graph.height}" opacity="0.45"/>'
    ]
    for n in graph.nodes:
        parts.append(f'<rect x="{n.x}" y="{n.y}" width="{n.w}" height="{n.h}" fill="none" stroke="red" stroke-width="3"/>')
        parts.append(f'<text x="{n.x+5}" y="{n.y+18}" font-family="Arial" font-size="14">{n.type}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def quality_report(graph) -> dict:
    nodes = graph.nodes
    overlaps = 0
    for i, a in enumerate(nodes):
        for b in nodes[i+1:]:
            ix = max(0, min(a.x+a.w, b.x+b.w)-max(a.x,b.x))
            iy = max(0, min(a.y+a.h, b.y+b.h)-max(a.y,b.y))
            if ix*iy > 0 and a.parent != b.id and b.parent != a.id:
                overlaps += 1
    return {
        "nodes": len(nodes),
        "overlap_pairs": overlaps,
        "with_parent": sum(1 for n in nodes if n.parent),
        "relations": len(graph.relations),
    }


def main():
    p = argparse.ArgumentParser(description="E2E screenshot -> detections -> LayoutGraph -> wireframe")
    p.add_argument("--image")
    p.add_argument("--detections", help="Use cached detector JSON instead of running vision")
    p.add_argument("--output", default="output/e2e")
    p.add_argument("--model", default="microsoft/Florence-2-large")
    args = p.parse_args()

    if not args.image and not args.detections:
        p.error("--image or --detections is required")

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    data = load_json(args.detections) if args.detections else extract_with_florence(args.image, args.model)
    (out/"detected.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    graph = image_to_layout(data["detections"], data["width"], data["height"])
    (out/"layout.json").write_text(json.dumps(graph.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    (out/"wireframe.svg").write_text(render_svg(graph), encoding="utf-8")
    (out/"report.json").write_text(json.dumps(quality_report(graph), indent=2), encoding="utf-8")

    if args.image:
        image = Path(args.image)
        target = out/image.name
        if image.resolve() != target.resolve():
            target.write_bytes(image.read_bytes())
        (out/"overlay.svg").write_text(overlay_svg(graph, image.name), encoding="utf-8")

    print(f"E2E artifacts written to {out}")


if __name__ == "__main__":
    main()
