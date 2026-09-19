# Wireproto structural benchmark

The benchmark exists to answer a concrete question: which observation stack reconstructs UI structure most faithfully for Wireproto?

It does **not** assume any model reaches 100% accuracy, and it does not replace the current Florence-2 pipeline. Florence-2 is the baseline. UI-TARS, Qwen2.5-VL, PaliGemma 2, CogAgent, SeeClick and future ensembles are experimental candidates that should be compared through the same canonical LayoutGraph.

## Metrics

- **BBox mean IoU** — geometric overlap of matched elements.
- **BBox IoU@0.50 accuracy** — fraction of matched nodes reaching IoU >= 0.50.
- **Component type accuracy** — semantic component classification.
- **Parent accuracy** — hierarchy reconstruction.
- **Relation precision / recall / F1** — recovery of graph edges such as above, left-of, aligned-left and equal-width.
- **Node coverage** — predicted, truth and matched node counts.

No single aggregate score is canonical. Keep the dimensions separate so a model that is strong at grounding but weak at hierarchy is visible as such.

## Ground truth

Each benchmark screenshot should have a hand-verified canonical LayoutGraph JSON. Stable node ids are used for the MVP matcher. Later versions can add assignment-based matching for adapters that cannot preserve ids.

Suggested fixture:

```text
benchmarks/
  landing-001/
    reference.png
    truth.json
    florence.json
    uitars.json
    qwen25vl.json
    paligemma2.json
    cogagent.json
    seeclick.json
```

## Evaluation loop

```text
reference screenshot
        |
        +--> current Florence-2 baseline
        +--> experimental adapter A
        +--> experimental adapter B
        +--> future ensemble
                    |
               LayoutGraph
                    |
              same constraints
                    |
              benchmark.py
                    |
       per-dimension metrics + preview
```

For fair comparisons, adapters must be evaluated on the same screenshots and converted to the same canonical graph contract. Constraint settings must also remain fixed.

## Future visual metric

Structural metrics should remain primary. A later benchmark stage can render each reconstructed graph into the same monochrome wireframe style and compare it with the verified wireframe using a visual similarity metric. This is complementary: visual similarity alone can hide hierarchy and semantic errors.

## Evolution strategy

1. Establish Florence-2 numbers as the baseline.
2. Add adapters without changing the existing pipeline.
3. Benchmark GUI-specialized and general vision models independently.
4. Analyze error categories instead of choosing from reputation or generic benchmarks.
5. Test observation fusion/ensemble only after individual baselines exist.
6. If enough verified examples accumulate, use prompt/image/graph triples for later distillation.
