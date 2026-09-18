import argparse, json
from pathlib import Path
from .pipeline import image_to_layout
from .renderer import render_svg

def main():
    parser=argparse.ArgumentParser(description="Reverse-engineer wireframe detections into a LayoutGraph")
    parser.add_argument("--detections",default="examples/detections.json")
    parser.add_argument("--output",default="output")
    args=parser.parse_args()
    data=json.loads(Path(args.detections).read_text(encoding="utf-8"))
    graph=image_to_layout(data["detections"],data.get("width",1440),data.get("height",900))
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    (out/"layout.json").write_text(json.dumps(graph.to_dict(),indent=2,ensure_ascii=False),encoding="utf-8")
    (out/"wireframe.svg").write_text(render_svg(graph),encoding="utf-8")
    print("Generated output/layout.json and output/wireframe.svg")

if __name__=="__main__": main()
