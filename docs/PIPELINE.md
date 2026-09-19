# Scene-graph-first reverse-engineering pipeline

The image model can remain a layout teacher, but pixels are never the canonical representation. The canonical artifact is a semantic UI scene graph recovered by Vision/VLM and repaired by deterministic constraints.

## Flow

1. Prompt or screenshot -> image/vision stage.
2. Vision/VLM structure parsing -> semantic candidates, text and approximate bounding boxes.
3. Scene graph construction -> hierarchy plus first-class spatial relationships.
4. Constraint normalization -> grid snapping, bounds, equal-size repair and parent containment.
5. Structural preview -> render the canonical graph as SVG for human inspection.
6. UI rendering -> use the validated graph/wireframe as the control structure for a renderer.
7. Dataset accumulation -> save prompt + source image + canonical graph + quality score for later distillation.

## Canonical contract

ASCII is intentionally not part of the pipeline. It loses geometry and makes hierarchy implicit.

A minimal adapter may emit:

```json
{"type":"card","bbox":[304,192,320,152],"confidence":0.95}
```

A semantic VLM adapter should prefer:

```json
{
  "id": "hero-copy",
  "type": "content-group",
  "bbox": [80, 160, 540, 420],
  "parent": "hero",
  "children": ["hero-title", "hero-cta"],
  "text": "",
  "layout": {"direction":"vertical","gap":16,"align":"left"},
  "constraints": {"grid":8},
  "visual_role": "primary-content",
  "confidence": 0.96
}
```

The canonical `LayoutGraph` stores viewport, nodes and graph-level relations. Nodes keep geometry and semantics; relations represent facts such as `above`, `left-of`, `aligned-left`, `aligned-y`, `equal-width` and `equal-height`.

## Responsibility split

**Vision/VLM:** discover what exists, approximate geometry, semantics, text and likely hierarchy.

**Relationship inference:** turn pairwise geometry into explicit graph edges and rebuild parent/children links.

**Constraint solver:** repair geometry deterministically. It must not invent UI semantics.

**Renderer:** consume the graph. SVG is only a preview, not the source of truth.

## Teacher prompt

When generating a synthetic wireframe teacher image, prefer a rigid visual language: black-and-white, low-fidelity UX wireframe, flat orthographic interface, no shadows or gradients, no decorative illustration, clear rectangular boundaries, consistent spacing and visible section separation.

## Next milestone

Add a semantic VLM adapter that emits the richer contract directly, then add row/column/repeated-group inference and structural quality scoring. Florence-2 remains useful as a lightweight detector fallback, not as the canonical representation.
