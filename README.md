# wireproto

Reverse-engineering prototype for high-quality AI-generated wireframes.

## Pipeline

```text
Prompt
  -> Image model (teacher)
  -> high-quality machine-readable wireframe image
  -> Vision/VLM structure parser
  -> semantic nodes + bbox + text + hierarchy hints
  -> Relationship inference
  -> canonical UI Scene Graph
  -> Deterministic constraint normalization
  -> scene-graph JSON + SVG preview
  -> dataset for later distillation
```

The goal is to reuse the layout knowledge already present in image/video models instead of training a layout generator from zero. The canonical representation is a semantic UI scene graph: nodes preserve bounding boxes, hierarchy, layout hints and constraints, while relationships such as alignment, containment and relative position live as first-class graph edges. SVG is not the generator; it is only a deterministic preview of that graph.

## Current MVP

The model-specific extraction boundary is provider-neutral JSON. A detector can provide only type + bbox, while a stronger VLM can additionally provide text, parent/children, layout hints, constraints and visual role. The pipeline never converts the structure to ASCII: geometry and semantics remain machine-readable end to end.

```bash
python -m wireproto.cli --detections examples/detections.json
```

Outputs:

- `output/layout.json`
- `output/wireframe.svg`

See `docs/PIPELINE.md` for the architecture and extraction contract.

## Next

Connect a real image generator, add vision/OCR adapters, infer rows/columns/repeated groups, add quality scoring, and persist prompt/image/graph triples as a synthetic training dataset for a future distilled Layout Transformer.


## E2E benchmark

Run the full reverse-engineering path directly from a screenshot:

```bash
pip install -e '.[vision]'
python -m wireproto.e2e --image reference.png --output output/reference
```

Artifacts:

- `detected.json` — raw vision detections
- `layout.json` — inferred canonical LayoutGraph
- `wireframe.svg` — reconstructed skeleton
- `overlay.svg` — detections over the source screenshot
- `report.json` — structural quality diagnostics

For fast development without loading the vision model, cache detections and rerun with `--detections output/reference/detected.json`.

The first benchmark target is the Flowly-style reference: feed the final UI screenshot and evaluate whether the reconstructed wireframe preserves its section hierarchy, columns, card groups, whitespace and major visual placeholders.


## Full generation E2E: left then right

The primary flow is now `prompt -> generated wireframe -> structure extraction -> LayoutGraph -> constrained control -> polished UI`.

```bash
wireproto-full-e2e "AI productivity landing page" \\
  --wireframe-command "./my-wireframe-adapter" \\
  --ui-command "./my-flux-controlnet-adapter"
```

Generator adapters receive `WIREPROTO_PROMPT` and `WIREPROTO_OUTPUT`. The UI adapter additionally receives `WIREPROTO_CONTROL_IMAGE`. This makes the pipeline provider-neutral while keeping the two stages explicit.

Artifacts are numbered in order: `01-wireframe.png` (left target), `02-detected.json`, `03-layout.json`, `04-constrained-wireframe.svg`, and `05-final-ui.png` (right target).
