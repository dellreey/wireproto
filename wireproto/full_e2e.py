import argparse,json,os
from pathlib import Path
from .generate_wireframe import generate_wireframe
from .vision import extract_with_florence
from .pipeline import image_to_layout
from .renderer import render_svg
from .render_ui import render_ui

def main():
    p=argparse.ArgumentParser(description="Prompt -> wireframe -> LayoutGraph -> constrained wireframe -> polished UI")
    p.add_argument("prompt"); p.add_argument("--output",default="output/full-e2e"); p.add_argument("--wireframe-command",default=os.getenv("WIREPROTO_WIREFRAME_COMMAND")); p.add_argument("--ui-command",default=os.getenv("WIREPROTO_UI_COMMAND")); p.add_argument("--model",default="microsoft/Florence-2-large"); p.add_argument("--wireframe")
    args=p.parse_args(); out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    wf=Path(args.wireframe) if args.wireframe else generate_wireframe(args.prompt,str(out/"01-wireframe.png"),args.wireframe_command)
    data=extract_with_florence(str(wf),args.model); (out/"02-detected.json").write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
    graph=image_to_layout(data["detections"],data["width"],data["height"]); (out/"03-layout.json").write_text(json.dumps(graph.to_dict(),indent=2,ensure_ascii=False),encoding="utf-8")
    control=out/"04-constrained-wireframe.svg"; control.write_text(render_svg(graph),encoding="utf-8")
    render_ui(args.prompt,str(control),str(out/"05-final-ui.png"),args.ui_command)
    (out/"manifest.json").write_text(json.dumps({"prompt":args.prompt,"wireframe":str(wf),"detections":"02-detected.json","layout":"03-layout.json","control":"04-constrained-wireframe.svg","final_ui":"05-final-ui.png"},indent=2,ensure_ascii=False),encoding="utf-8")
    print("Full E2E artifacts written to "+str(out))

if __name__=="__main__": main()
