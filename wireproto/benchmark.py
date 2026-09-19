"""Structural benchmark metrics for Wireproto scene graphs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .schema import LayoutGraph, Node, Relation


def bbox_iou(a: Node, b: Node) -> float:
    x1=max(a.x,b.x); y1=max(a.y,b.y)
    x2=min(a.x+a.w,b.x+b.w); y2=min(a.y+a.h,b.y+b.h)
    inter=max(0,x2-x1)*max(0,y2-y1)
    union=a.w*a.h+b.w*b.h-inter
    return inter/union if union else 0.0


def _matched(pred: LayoutGraph, truth: LayoutGraph):
    """Match by stable node id. Benchmark fixtures should preserve ids."""
    p={n.id:n for n in pred.nodes}
    t={n.id:n for n in truth.nodes}
    ids=sorted(p.keys() & t.keys())
    return [(p[i],t[i]) for i in ids]


def evaluate(pred: LayoutGraph, truth: LayoutGraph) -> dict:
    pairs=_matched(pred,truth)
    ious=[bbox_iou(p,t) for p,t in pairs]

    type_correct=sum(p.type==t.type for p,t in pairs)
    parent_correct=sum(p.parent==t.parent for p,t in pairs)

    pred_rel={(r.type,r.source,r.target) for r in pred.relations}
    truth_rel={(r.type,r.source,r.target) for r in truth.relations}
    tp=len(pred_rel & truth_rel)
    precision=tp/len(pred_rel) if pred_rel else (1.0 if not truth_rel else 0.0)
    recall=tp/len(truth_rel) if truth_rel else 1.0
    f1=2*precision*recall/(precision+recall) if precision+recall else 0.0

    return {
        "matched_nodes": len(pairs),
        "pred_nodes": len(pred.nodes),
        "truth_nodes": len(truth.nodes),
        "bbox_mean_iou": sum(ious)/len(ious) if ious else 0.0,
        "bbox_iou_50_accuracy": sum(v>=0.5 for v in ious)/len(ious) if ious else 0.0,
        "component_type_accuracy": type_correct/len(pairs) if pairs else 0.0,
        "parent_accuracy": parent_correct/len(pairs) if pairs else 0.0,
        "relation_precision": precision,
        "relation_recall": recall,
        "relation_f1": f1,
    }
