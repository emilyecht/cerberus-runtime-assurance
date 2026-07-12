# CERBERUS White Paper Update

## From matched-model pipeline verification to robustness mapping and executable structural FCOI

**Author:** Emily Echterhoff  
**Status:** Research and planning update  
**Date:** July 2026

> **Intelligence is not safety. Layering is not independence. Independence is not permanent.**

## Executive summary

CERBERUS treats the failure-mode independence of layered assurance mechanisms as a perishable runtime quantity. The v3.5 manuscript establishes the architecture, evidence hierarchy, authority law, bounded recovery discipline, and a reproducible matched-model experiment. This update defines the next two research milestones without claiming that either is already implemented:

1. **CERBERUS Stress Suite v1** — a pre-registered synthetic robustness program that intentionally breaks the match between the Vigil detector and the data generator.
2. **Structural FCOI Engine v1** — an auditable design-time engine that computes minimal-cut-set overlap from explicit Boolean fault logic while refusing to treat missing structure as independence.

The sequence is deliberate. Stress Suite v1 first tests the behavior of the currently implemented evidence-to-authority pipeline under mismatch and degraded telemetry. Structural FCOI Engine v1 then turns the central design-time overlap quantity into executable, reviewable tooling.

This document is a planning artifact. It adds no new operational, flight-readiness, certification, or realistic-detection claim.

## Verified baseline

The maintained experiment is a fixed-seed matched-model pipeline verification. Two synthetic channels share a measured environment; a latent common process is injected after a known onset; Vigil conditions on the measured environment, monitors rolling residual correlation, computes a one-sided Fisher upper confidence bound, applies persistence, and maps adverse evidence to illustrative authority contraction.

| Metric | Verified result |
|---|---:|
| Calibrated alarm threshold | **0.45832639152918053** |
| Rounded threshold used in the READMEs | **0.458326** |
| Nominal sustained-alarm runs | **0 / 200** |
| Two-sided 95% exact upper bound on nominal run-alarm rate | **1.83%** |
| Coupling detections | **200 / 200** |
| Two-sided 95% exact lower bound on coupling detection rate | **98.17%** |
| Median detection sample | **1061.5** |
| Median lead before the defined symptom | **238.5 samples** |
| 10th–90th percentile lead | **160.9–319.6 samples** |
| Representative detection sample | **984** |

These results verify that the supplied matched-model pipeline is wired consistently and reproducibly. They do **not** establish zero false alarms, perfect operational detection, causal discovery, model-mismatch robustness, realistic telemetry performance, full probabilistic FCOI, spacecraft fault-detection performance, or flight authority validity.

## Milestone 1 — CERBERUS Stress Suite v1

### Research question

How does the present Vigil evidence-to-authority pipeline behave when the detector no longer matches the generator, telemetry is degraded, and benign operational changes can resemble harmful coupling?

### Experimental discipline

Stress Suite v1 will use three separated seed partitions:

1. **Calibration partition** — calibrates detector thresholds to a common nominal run-level alarm budget.
2. **Development partition** — supports generator debugging, detector debugging, and exploratory severity selection.
3. **Frozen confirmatory partition** — is hashed and evaluated only after detectors, thresholds, metrics, and reporting rules are frozen.

All detectors receive identical generated runs and seeds for paired comparison. Confirmatory results cannot be used to retune the reported protocol without declaring a new version.

### Planned stress families

- missing, bursty, duplicated, stale, reordered, and channel-specific telemetry;
- timestamp jitter, drift, offsets, latency, and channel misalignment;
- variance ramps, heavy tails, outliers, autocorrelation, quantization, and clipping;
- nonlinear, biased, delayed, degraded, or incomplete environmental conditioning;
- benign unmodeled common stimuli and maneuver-like transients;
- abrupt, gradual, intermittent, low-and-slow, oscillatory, sign-changing, and condition-dependent harmful coupling;
- selected compound cases such as coupling plus dropout or clock drift plus a benign common stimulus.

### Planned detector set

1. Current conditioned residual Pearson correlation with Fisher upper bound and persistence.
2. Conditioned residual Spearman rank correlation.
3. CUSUM on a frozen residual-dependence statistic.
4. Page–Hinkley on the same statistic.
5. A simple conservative ensemble whose agreement may demote but may not create authority.

### Required outputs

- run-level false-alarm and detection rates with confidence intervals;
- detection sample, lead time, and minimum detectable coupling severity;
- evidence-invalid and evidence-unknown fractions;
- authority-state occupancy, chattering, demotion latency, and recovery latency;
- prolonged-A0 behavior under benign ambiguity;
- a published failure gallery and robustness map, including negative results.

### Hard invariants

Regardless of detector performance:

- invalid, stale, inconsistent, or non-estimable evidence must never increase authority;
- worsening evidence must never cause promotion;
- confirmatory seeds must never tune the detector;
- identical seeds and configuration must reproduce identical summaries;
- the original matched-model reproduction must remain unchanged;
- negative results must remain visible.

The detailed plan is maintained in the experiment repository:

- [CERBERUS Stress Suite v1 Research Plan](https://github.com/emilyecht/cerberus-vigil-experiment/blob/main/docs/CERBERUS_Stress_Suite_v1_Research_Plan.md)

## Milestone 2 — Structural FCOI Engine v1

### Research question

Can structural FCOI be computed deterministically from a versioned, reviewable fault model while refusing to convert incomplete structure into false independence?

### Key modeling decision

A directed causal graph alone is insufficient to derive minimal cut sets. Reachability shows that a mechanism can influence a failure, but it does not specify whether causes are individually sufficient, jointly sufficient, or alternatives.

Structural FCOI Engine v1 therefore separates:

1. **Causal evidence graph** — root causes, environmental variables, propagation mechanisms, terminal layer failures, and evidence references.
2. **Boolean sufficiency model** — basic events, AND/OR gates, and a top event for each layer and failure class.

### Reference algorithm

The first implementation should remain deliberately simple and auditable:

- a basic event produces a singleton cut set;
- an OR gate unions child cut-set families;
- an AND gate forms the Cartesian product of child families and unions the members of each product;
- every step canonicalizes sets, removes duplicates, and removes strict supersets of existing cut sets.

This reference implementation remains the correctness oracle even if a BDD or ZDD backend is added later for scale.

### Structural FCOI

For layer pair \(i,j\) and failure class \(k\):

```math
\mathrm{FCOI}^{S}_{ij,k}=
\frac{|M_{i,k}\cap M_{j,k}|}
{|M_{i,k}\cup M_{j,k}|}.
```

Required semantics:

- canonical cut sets are compared by root-cause identity;
- repeated propagation paths that reduce to the same minimal cut set count once;
- when both cut-set families are empty, the result is **not estimable**, not zero;
- exact structural FCOI is a design-time screening quantity, not a runtime authority command.

### Near-match census

Exact equality can miss structurally similar cut sets. v1 therefore reports, separately from exact FCOI:

- one-substitution pairs;
- one-added or one-removed-root pairs;
- maximum pairwise set-Jaccard similarity;
- shared root-cause incidence across families;
- top near-match pairs with mechanism traces.

Near matches remain visible and are not compressed into an opaque score that could flatter the model.

### Validation burden

The validation corpus will include identical, disjoint, partial, empty, repeated-path, dominated-superset, nested AND/OR, strong-near-match, undeveloped-event, and invalid-model examples. Small models will be independently cross-checked by truth-table enumeration and property tests for determinism, permutation invariance, duplicate-path invariance, and conservative unknown handling.

The detailed plan is maintained in this repository:

- [Structural FCOI Engine v1 Research Plan](Structural_FCOI_Engine_v1_Research_Plan.md)

## Ordered research gates

1. Freeze the Stress Suite protocol, claim boundary, scenario taxonomy, detector interfaces, seed partitions, and hard invariants.
2. Implement and run exploratory screening without touching the held-out confirmatory partition.
3. Freeze acceptance criteria and run the confirmatory Stress Suite evaluation once.
4. Publish the robustness map, failure gallery, and non-claims.
5. Freeze the structural FCOI causal and Boolean semantics.
6. Build the auditable reference cut-set engine and validation corpus.
7. Add exact FCOI, near-match reporting, mechanism traces, and deterministic exports.
8. Consider optimized backends, probabilistic FCOI, graph-external witnesses, and HIL work only after the v1 evidence boundaries are satisfied.

## Updated implementation boundary

| Artifact or mechanism | Current status | Next evidence target |
|---|---|---|
| Matched-model Vigil experiment | Implemented and reproducible | Preserve as the baseline regression target |
| Stress Suite v1 | Planned, not implemented | Synthetic model-mismatch robustness map |
| Structural FCOI Engine v1 | Planned, not implemented | Hand-verified minimal-cut-set overlap tooling |
| Probabilistic FCOI estimator | Specified, not implemented | Future calibrated root-cause and marginal-failure model |
| Graph-external witness | Proposed | Separate representation and one-way authority effect |
| Flight/HIL validation | Future work | No current certification, TRL, or operational-readiness claim |

## Conclusion

CERBERUS is strongest when it refuses to confuse successful demonstration with finished assurance. The matched-model experiment supplies a reproducible baseline. Stress Suite v1 will try to break that pipeline honestly and map where it bends. Structural FCOI Engine v1 will give the architecture an executable design-time skeleton that treats unknown structure as unknown rather than independent.

The governing discipline remains:

> **define independence → measure drift → challenge omissions → budget authority → demote quickly → restore slowly**
