# Reverse-engineering pipeline

Fast path: use an image model as the layout teacher instead of training a layout model first.

## Flow

1. Prompt -> image model: generate a deliberately machine-readable low-fidelity wireframe.
2. Structure extraction: vision/detection/OCR returns semantic candidates and bounding boxes.
3. Relationship inference: containment, hierarchy, alignment and relative position.
4. Constraint pass: snap geometry to grid and repair bounds.
5. LayoutGraph: canonical machine-readable representation.
6. Renderer: SVG is only a preview.
7. Dataset accumulation: save prompt + generated image + LayoutGraph + quality score for later distillation.

## Extraction contract

Detector adapters output objects such as `{"type":"card","bbox":[304,192,320,152],"confidence":0.95}` where bbox is x,y,width,height. This keeps Florence-2, detection models, OCR systems and future adapters interchangeable.

## Teacher prompt

Prefer a rigid visual language: black-and-white, low-fidelity UX wireframe, flat orthographic interface, no shadows or gradients, no decorative illustration, clear rectangular boundaries, consistent spacing and visible section separation.

## Next milestone

Add a real image-model adapter and a real structure-extractor adapter. The core graph intentionally does not depend on a specific provider.
