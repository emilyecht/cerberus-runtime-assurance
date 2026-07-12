# Structural FCOI Engine v1 Research Plan

**Status:** Planning only; no implementation is claimed.  
**Parent architecture:** CERBERUS v3.5  
**Primary tracking issue:** [#1 — Implement the structural FCOI minimal-cut-set engine](https://github.com/emilyecht/cerberus-runtime-assurance/issues/1)

## Purpose

Structural FCOI Engine v1 will turn the design-time structural form of the Failure-Cause Overlap Index into deterministic, reviewable tooling. The engine must compute minimal-cut-set overlap without treating missing model structure as independence.

The v1 claim is intentionally narrow:

> Given an explicit, validated Boolean fault model, compute exact minimal-cut-set families and a transparent structural-overlap report.

It is not a probabilistic FCOI estimator, runtime authority controller, causal-discovery system, or certification tool.

## Critical semantic split

A causal graph and a fault-logic model serve different purposes and must not be silently conflated.

### Causal evidence graph

Records:

- root causes;
- environmental variables;
- propagation mechanisms;
- terminal layer failures;
- evidence references and review status.

This graph explains why a modeled dependency exists.

### Boolean sufficiency model

Defines:

- basic events;
- AND/OR gates;
- top event for each layer and failure class;
- which combinations are sufficient to raise a failure indicator.

This model determines minimal cut sets.

## v1 scope

### Included

- static acyclic AND/OR fault logic;
- typed and versioned nodes;
- deterministic schema and semantic validation;
- exact minimal-cut-set enumeration for small and moderate examples;
- duplicate and dominated-superset removal;
- exact-match structural FCOI;
- explicit near-match census;
- reviewable mechanism traces;
- JSON and tabular exports;
- hand-calculated and truth-table validation fixtures.

### Excluded

- dynamic fault-tree gates;
- sequence-dependent failures;
- repairable-state models;
- probabilistic FCOI;
- Bayesian parameter updating;
- runtime authority changes;
- Sentinel evidence;
- operational or certification claims.

## Proposed model schema

Each model should declare:

- model ID and semantic version;
- failure-class ID;
- layer IDs;
- typed node IDs;
- basic-event definitions;
- AND/OR gate definitions;
- top event per layer;
- causal mechanism references;
- evidence status;
- assumptions;
- explicitly undeveloped events;
- deterministic content hash.

### Node types

- `root_cause`
- `environment`
- `propagation`
- `basic_event`
- `and_gate`
- `or_gate`
- `terminal_failure`
- `undeveloped`
- `unknown`

## Conservative validation behavior

- Missing top event: invalid model.
- Unknown gate type: unsupported, never approximated.
- Cycle: invalid model.
- Missing referenced node: invalid model.
- Both cut-set families empty: `not_estimable`.
- One family empty and one nonempty: exact overlap `0.0`, with the empty family reported explicitly.
- Incomplete evidence: visible in output and never interpreted as demonstrated independence.
- Undeveloped events: retained in every relevant report.

## Reference minimal-cut-set algorithm

The first engine should be a deliberately simple correctness oracle.

For each node, compute an antichain of canonical root-cause sets:

- basic event: `{{event}}`;
- OR gate: union child families;
- AND gate: Cartesian product of child families, followed by set union;
- after each operation:
  - canonicalize every set;
  - remove duplicate sets;
  - remove every strict superset of another set.

Repeated propagation paths that reduce to the same minimal root-cause set count once.

A later BDD or ZDD backend may improve scalability, but it must be cross-checked against this reference implementation and may not replace it as the only source of truth.

## Structural FCOI

For layer pair `(i, j)` and failure class `k`:

```math
\mathrm{FCOI}^{S}_{ij,k} =
\frac{|M_{i,k}\cap M_{j,k}|}
{|M_{i,k}\cup M_{j,k}|}.
```

Rules:

- compare canonical root-cause sets;
- count each unique minimal cut set once;
- return `not_estimable` when the union is empty;
- report exact FCOI as a design-time screening value, not an authority command.

## Near-match census

Near matches remain separate from exact FCOI in v1.

Report:

- exact matches;
- equal-size pairs differing by one substituted root cause;
- pairs with one added or removed root cause;
- maximum pairwise set-Jaccard similarity;
- pairwise-similarity distribution;
- shared root-cause incidence across both families;
- top near-match pairs with mechanism trace.

A weighted refinement may be researched later. v1 must not compress near-match evidence into an opaque score.

## Validation corpus

### Hand-calculated fixtures

1. Identical families → `1.0`.
2. Disjoint families → `0.0`.
3. Partial family overlap.
4. One empty and one nonempty family → `0.0` plus explicit empty-family status.
5. Both empty → `not_estimable`.
6. Repeated paths collapsing to one cut set.
7. Dominated supersets removed.
8. Nested AND/OR logic.
9. Common root cause through different propagation nodes.
10. Exact-match zero with strong near-match warning.
11. Undeveloped event retained.
12. Invalid or incomplete model rejected or flagged.

### Independent cross-checks

For sufficiently small models:

- enumerate all truth assignments;
- identify assignments that raise the top event;
- derive minimal satisfying assignments independently;
- compare them with the reference cut-set engine.

### Property tests

- input ordering does not change output;
- node renaming does not change metric values;
- adding a dominated superset does not change the minimal family;
- duplicating a path does not change FCOI;
- invalid structure never produces a numeric zero;
- output hashes and reports are deterministic.

## Proposed repository structure

```text
docs/fcoi-engine-v1/
  semantics.md
  input-schema.md
  cut-set-algorithm.md
  near-match-policy.md
  validation-plan.md
  evidence-boundary.md

schemas/
  fcoi-model.schema.json
  fcoi-report.schema.json

examples/fcoi/
  identical/
  disjoint/
  partial-overlap/
  repeated-path/
  strong-near-match/
  invalid-models/

src/cerberus_fcoi/
  model.py
  schema.py
  validate.py
  cutsets.py
  metrics.py
  near_match.py
  trace.py
  report.py
  cli.py

tests/fcoi/
  test_schema.py
  test_cutsets_hand_examples.py
  test_fcoi_metrics.py
  test_near_match.py
  test_truth_table_crosscheck.py
  test_properties.py
  test_invalid_models.py
```

## Proposed issue sequence

1. **FCOI-01 — Freeze causal and Boolean semantics**
2. **FCOI-02 — Specify versioned input and report schemas**
3. **FCOI-03 — Build the auditable reference cut-set algorithm**
4. **FCOI-04 — Implement exact structural FCOI semantics**
5. **FCOI-05 — Define and validate the near-match census**
6. **FCOI-06 — Build the hand-calculated validation corpus**
7. **FCOI-07 — Add truth-table and property-based cross-checks**
8. **FCOI-08 — Specify reviewable mechanism traces and exports**
9. **FCOI-09 — Evaluate BDD/ZDD optimization against the reference oracle**
10. **FCOI-10 — Publish the v1 evidence boundary and non-claims**

## Exit criteria

Structural FCOI Engine v1 is complete only when:

- every documented hand calculation is reproduced;
- all small models pass independent truth-table cross-checks;
- exact-match and near-match results remain separate;
- empty, unknown, or incomplete models cannot silently return demonstrated independence;
- repeated paths do not double-count cut sets;
- every report includes model version and content hash;
- outputs are deterministic and permutation invariant;
- the reference algorithm remains available if an optimized backend is introduced;
- the release claim remains **design-time structural screening tool**, not probabilistic or operational validation.
