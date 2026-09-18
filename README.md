# wireproto

Reverse-engineering prototype for high-quality AI-generated wireframes.

## Pipeline

```text
Prompt
  -> Image model (teacher)
  -> high-quality machine-readable wireframe image
  -> Structure extractor (vision/detection/OCR)
  -> [type, x, y, w, h, confidence]
  -> Relationship inference
  -> LayoutGraph
  -> Constraint pass
  -> JSON + SVG preview
  -> dataset for later distillation
```

The goal is to reuse the layout knowledge already present in image/video models instead of training a layout generator from zero. SVG is not the generator; it is only a deterministic preview of the recovered structure.

## Current MVP

The model-specific extraction boundary is represented by a simple detection JSON contract. This lets us test extraction -> relationships -> constraints -> graph -> renderer immediately, then plug Florence-2 or another vision stack into the same contract.

```bash
python -m wireproto.cli --detections examples/detections.json
```

Outputs:

- `output/layout.json`
- `output/wireframe.svg`

See `docs/PIPELINE.md` for the architecture and extraction contract.

## Next

Connect a real image generator, add vision/OCR adapters, infer rows/columns/repeated groups, add quality scoring, and persist prompt/image/graph triples as a synthetic training dataset for a future distilled Layout Transformer.
