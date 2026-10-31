# Copyright 2026 Emily Echterhoff
# SPDX-License-Identifier: MIT

"""Exact bounded antichains for explicit monotone Boolean fault models.

Root-cause IDs are Boolean variables, not discovered causal facts. No probability,
runtime monitoring, near-match weighting or authority mechanism lives here.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
from importlib.resources import files
from itertools import chain, combinations
import json

from jsonschema import Draft202012Validator


class ModelError(ValueError):
    """An invalid or unsupported model must never become numeric independence."""


class EnumerationLimit(ModelError):
    """Exact work exceeded an explicit budget; no truncated result is returned."""


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ModelError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_model(text: str) -> dict:
    def nonfinite(value):
        raise ModelError(f"non-finite JSON value: {value}")
    try:
        return json.loads(text, object_pairs_hook=_object, parse_constant=nonfinite)
    except (ValueError, TypeError) as exc:
        raise ModelError(str(exc)) from exc


def _validated(model):
    schema = json.loads(files("cerberus_fcoi").joinpath("model-v1.schema.json").read_text())
    errors = sorted(Draft202012Validator(schema).iter_errors(model), key=lambda e: str(list(e.path)))
    if errors:
        error = errors[0]
        raise ModelError(f"schema violation at {list(error.path)}: {error.message}")
    data = deepcopy(model)
    nodes = {n["id"]: n for n in data["nodes"]}
    causes = {c["id"] for c in data["root_causes"]}
    if len(nodes) != len(data["nodes"]) or len(causes) != len(data["root_causes"]):
        raise ModelError("duplicate node or root-cause ID")
    for node in nodes.values():
        if node["type"] == "basic_event" and node["root_cause"] not in causes:
            raise ModelError(f"missing root cause for {node['id']}")
        for child in node.get("inputs", []):
            if child not in nodes:
                raise ModelError(f"missing node: {child}")
    if any(top not in nodes for top in data["top_events"].values()):
        raise ModelError("missing top event")
    order, active, done = [], set(), set()

    def visit(node_id):
        if node_id in active:
            raise ModelError(f"cycle at {node_id}")
        if node_id in done:
            return
        active.add(node_id)
        for child in sorted(nodes[node_id].get("inputs", [])):
            visit(child)
        active.remove(node_id)
        done.add(node_id)
        order.append(node_id)

    # Validate all nodes, including unreachable cycles/unsupported references.
    for node_id in sorted(nodes):
        visit(node_id)
    for node in data["nodes"]:
        node["mechanism_refs"].sort()
        if "inputs" in node:
            node["inputs"].sort()
    for cause in data["root_causes"]:
        cause["evidence_refs"].sort()
    data["nodes"].sort(key=lambda n: n["id"])
    data["root_causes"].sort(key=lambda n: n["id"])
    data["assumptions"].sort()
    data["undeveloped_events"].sort()
    return data, {n["id"]: n for n in data["nodes"]}, order


def _cut_order(cut):
    return len(cut), tuple(sorted(cut))


def _families(nodes, order, max_cut_sets, max_candidates):
    remaining = max_candidates

    def minimize(candidates):
        nonlocal remaining
        kept = set()
        for cut in candidates:
            remaining -= 1
            if remaining < 0:
                raise EnumerationLimit("candidate budget exceeded; no partial enumeration returned")
            if any(existing <= cut for existing in kept):
                continue
            kept = {existing for existing in kept if not cut < existing}
            kept.add(cut)
            if len(kept) > max_cut_sets:
                raise EnumerationLimit("cut-set budget exceeded; no partial enumeration returned")
        return tuple(sorted(kept, key=_cut_order))

    result = {}
    for node_id in order:
        node = nodes[node_id]
        kind = node["type"]
        if kind == "basic_event":
            family = minimize([frozenset({node["root_cause"]})])
        elif kind == "constant":
            family = minimize([frozenset()] if node["value"] else [])
        elif kind == "or_gate":
            family = minimize(chain.from_iterable(result[c] for c in node["inputs"]))
        else:  # The schema admits only and_gate here.
            family = (frozenset(),)
            for child in node["inputs"]:
                family = minimize(a | b for a in family for b in result[child])
        result[node_id] = family
    return result


def analyze_model(model: dict, *, max_cut_sets: int = 1024, max_candidates: int = 100000) -> dict:
    for value in (max_cut_sets, max_candidates):
        if type(value) is not int or value < 1:
            raise ModelError("enumeration budgets must be positive integers")
    data, nodes, order = _validated(model)
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    warnings = ["Model-relative design-time screening; zero exact overlap does not establish independence.",
                "Evidence review status is a model declaration, not independently verified by this tool."]
    incomplete = data["evidence_status"] == "incomplete" or bool(data["undeveloped_events"])
    if incomplete:
        warnings.append("Incomplete evidence or undeveloped events: no numeric overlap is issued.")
    computed = {} if incomplete else _families(nodes, order, max_cut_sets, max_candidates)
    layers = {}
    for layer, top in sorted(data["top_events"].items()):
        family = computed.get(top)
        layers[layer] = {
            "top_event": top,
            "minimal_cut_sets": None if family is None else [sorted(cut) for cut in family],
            "unconditional_failure": None if family is None else frozenset() in family,
        }
        if family is not None and frozenset() in family:
            warnings.append(f"{layer}: empty cut set denotes unconditional failure, not missing evidence.")
    pairs = []
    for first, second in combinations(layers, 2):
        a, b = (computed.get(data["top_events"][layer]) for layer in (first, second))
        if a is None or b is None:
            numerator, denominator, ratio, shared = None, None, None, []
        else:
            intersection, union = set(a) & set(b), set(a) | set(b)
            numerator, denominator = len(intersection), len(union)
            ratio = numerator / denominator if denominator else None
            shared = sorted(set(chain.from_iterable(a)) & set(chain.from_iterable(b)))
        pairs.append({"layers": [first, second], "status": "not_estimable" if ratio is None else "model_relative",
                      "intersection_count": numerator, "union_count": denominator,
                      "exact_structural_fcoi": ratio, "shared_root_causes": shared,
                      "empty_families": [] if incomplete else [layer for layer, family in ((first, a), (second, b)) if not family]})
    return {
        "report_version": "0.1.0", "model_schema_version": data["schema_version"],
        "model_id": data["model_id"], "model_version": data["model_version"],
        "failure_class": data["failure_class"], "normalized_model_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
        "analysis_kind": "design-time-structural-screening", "evidence_status": data["evidence_status"],
        "assumptions": data["assumptions"], "undeveloped_events": data["undeveloped_events"],
        "mechanism_refs": {node_id: node["mechanism_refs"] for node_id, node in sorted(nodes.items())},
        "limits": {"max_cut_sets": max_cut_sets, "max_candidates": max_candidates},
        "layers": layers, "pairs": pairs, "warnings": warnings,
    }
