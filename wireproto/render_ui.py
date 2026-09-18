import os, subprocess
from pathlib import Path
from .prompts import ui_prompt

def render_ui(prompt, control_image, output, command=None):
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True)
    if not command: raise RuntimeError("No UI renderer configured. Pass --ui-command or set WIREPROTO_UI_COMMAND.")
    env=os.environ.copy(); env["WIREPROTO_PROMPT"]=ui_prompt(prompt); env["WIREPROTO_CONTROL_IMAGE"]=str(control_image); env["WIREPROTO_OUTPUT"]=str(out)
    subprocess.run(command,shell=True,check=True,env=env)
    if not out.exists(): raise RuntimeError("UI renderer did not create "+str(out))
    return out
