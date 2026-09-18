"""Vision adapters for E2E screenshot -> detections.

Florence-2 is optional and loaded only when requested.
"""
import json
from pathlib import Path


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def extract_with_florence(image_path: str, model_id: str = "microsoft/Florence-2-large") -> dict:
    try:
        import torch
        from PIL import Image
        from transformers import AutoModelForCausalLM, AutoProcessor
    except ImportError as exc:
        raise RuntimeError("Install optional vision deps: pip install -e '.[vision]'") from exc

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype=dtype).to(device)
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
    image = Image.open(image_path).convert("RGB")
    task = "<OD>"
    inputs = processor(text=task, images=image, return_tensors="pt")
    inputs = {k: v.to(device) if hasattr(v, "to") else v for k, v in inputs.items()}
    generated = model.generate(**inputs, max_new_tokens=1024, num_beams=3)
    text = processor.batch_decode(generated, skip_special_tokens=False)[0]
    parsed = processor.post_process_generation(text, task=task, image_size=image.size)
    od = parsed.get(task, parsed)

    detections = []
    for i, (box, label) in enumerate(zip(od.get("bboxes", []), od.get("labels", []))):
        x1, y1, x2, y2 = box
        detections.append({
            "id": f"det-{i}",
            "type": str(label).lower().replace(" ", "-"),
            "label": str(label),
            "bbox": [x1, y1, x2-x1, y2-y1],
            "confidence": 1.0,
        })
    return {"width": image.width, "height": image.height, "detections": detections}
