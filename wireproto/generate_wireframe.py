import os, subprocess
from pathlib import Path
from .prompts import wireframe_prompt

def generate_wireframe(prompt, output, command=None):
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True)
    if not command: raise RuntimeError("No image generator configured. Pass --wireframe-command or set WIREPROTO_WIREFRAME_COMMAND.")
    env=os.environ.copy(); env["WIREPROTO_PROMPT"]=wireframe_prompt(prompt); env["WIREPROTO_OUTPUT"]=str(out)
    subprocess.run(command,shell=True,check=True,env=env)
    if not out.exists(): raise RuntimeError("Wireframe generator did not create "+str(out))
    return out
