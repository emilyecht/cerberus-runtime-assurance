# Structural FCOI — Boolean Vertical Slice 0.1.0

**Implemented design-time research slice, not the complete Structural FCOI Engine
v1, probabilistic FCOI, runtime authority control or a flight safety case.**
CERBERUS Protocol and CERBERUS Cyber remain separate projects and evidence bases.

## Frozen Boolean contract

Input schema **1.0.0** lives at `src/cerberus_fcoi/model-v1.schema.json`.
Its exact-byte SHA-256 is recorded in `schemas/fcoi-model-v1.sha256` and tested.
Semantic changes require a new schema version, not silent reinterpretation of
old fixtures. Model semantic versions are separate numeric major.minor.patch.

The input declares model/failure-class IDs, assumptions, evidence status,
undeveloped events, root causes, typed nodes and a top event per named layer.
Types are `basic_event`, `and_gate`, `or_gate` and explicit Boolean `constant`.
At least two layer tops are required. This is a static, monotone, acyclic Boolean
sufficiency model, **not a causal evidence graph**.

- A root-cause ID is a Boolean variable. Distinct basic-event nodes may reference
  the same variable to model repeated paths; this causal identity is an assumption,
  not discovered or validated by the tool.
- Basic event: `{{cause}}`. OR: union child families. AND: unions across Cartesian
  products. Duplicates and strict supersets are absorbed into a deterministic antichain.
- Explicit `false` has family `[]`: no sufficient assignment. Explicit `true`
  has `[[]]`: the empty cut set, meaning unconditional failure. Neither represents
  missing evidence; an empty family and an empty cut set are different.
- Exact FCOI is identical cut-set intersection count / union count. Both families
  empty gives `not_estimable` and null score. One empty/nonempty gives zero with
  an explicit empty-family flag.
- Incomplete evidence or declared undeveloped events suppress enumeration and
  numeric overlap. Unknown fields/types/gates, references, missing tops, duplicate
  IDs/JSON keys, cycles (even unreachable), versions and non-finite JSON fail
  validation instead of producing zero.

Evidence refs and review status are declarations, not verified observations.
Unreviewed complete Boolean examples are calculable but cannot establish
independence. Every report warns that zero exact overlap is not independence.
Shared root incidence is separate; full near-match census, weighting and reviewed
causal mechanism tracing remain future work.

## Run and reproduce

```bash
python -m pip install .
python -m cerberus_fcoi examples/fcoi/partial-overlap.json
python -m unittest discover -s tests/fcoi -v
```

The example compares `{{A},{B}}` and `{{B},{C}}`: intersection 1, union 3,
score 1/3. Output is deterministic JSON. Invalid models and exceeded budgets exit
**2** with no stdout report; partial enumeration is never returned as an exact
score. The CLI reads local data, contacts no service, executes no model code and
changes no runtime authority or model file.

Defaults permit 1,024 retained cut sets per node and 100,000 candidate visits
overall. Schema bounds: 128 nodes, 32 causes, 32 inputs per gate, 16 layers.
Worst-case growth is exponential; no scalability claim. The budget can be reached
before a later absorption would reduce a family, still yielding no partial result.

Normalization sorts semantic collections/JSON keys for `normalized_model_sha256`.
Reordering nodes, causes or gate children preserves report/hash. Renaming nodes
changes provenance/hash, not the metric. This is Python normalization, not an
adopted cross-language canonicalization standard.

## Validation and limits

`examples/fcoi/hand-calculated.json` gives ten explicit calculations: identical,
disjoint, partial, nested absorption, dominated supersets, repeated root paths,
shared-root near matches with zero exact overlap, one/both empty families and
unconditional failure. Tests use a separately implemented exhaustive truth-table
oracle and 60 fixed-seed small DAGs with two layer outputs each; they also check
ordering, renaming, invalid/incomplete models, unchanged caller input, schema
bytes, budgets and CLI determinism. This is project-authored validation, **not an
independent third-party review**.

No probability, real causal completeness, runtime independence, certification,
flight readiness, formal verification, HIL or Cyber performance is established.
A schema cannot repair omitted shared causes. The v3.5 manuscript's historical
implementation boundary stays unchanged; the current README/inventory identify
this bounded slice.
