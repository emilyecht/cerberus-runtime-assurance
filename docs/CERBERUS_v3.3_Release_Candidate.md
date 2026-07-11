# CERBERUS v3.3

## The Fourth Guarantee: Independence as a Runtime Quantity

**Emily Echterhoff**  
Working release candidate — research architecture, not flight-certified software

> Intelligence is not safety. Layering is not independence. Independence is not permanent.

## Abstract

CERBERUS is a three-layer runtime-assurance architecture for autonomous systems. An adaptive **Pilot** proposes actions but never holds direct execution authority; a deterministic **Watchdog** checks proposals against physics invariants and certified envelopes; and a minimal **Anchor** preserves a mission-survivable floor. A non-authoritative **Vigil** estimates whether the layers remain failure-mode independent over mission life.

The central claim is that inter-layer independence should not be treated as a permanent design-time fact. It is a perishable runtime quantity that can decay through aging, maintenance, shared environmental stress, software convergence, compromised ground commands, or newly discovered common-cause pathways. CERBERUS therefore models independence, monitors it, adversarially challenges it, budgets authority against its pessimistic estimate, and restores authority only through fresh evidence.

## 1. Architecture

### Pilot

The Pilot performs adaptive reasoning, planning, and hypothesis generation. It may inspect Watchdog constraints and pre-shape proposals, but it cannot execute commands or relax constraints.

### Watchdog

The Watchdog is a deterministic gate. It evaluates proposals against physics invariants, hard envelopes, certified rules, and required cross-channel agreement. Its value is not greater intelligence; its value is failing for different reasons than the Pilot.

### Anchor

The Anchor enforces the minimum mission-survivable action set: power-positive attitude, thermal survival, bounded orientation control, authenticated communications, and an evidence-gated route to recovery. Anchor invariants are not overridable by Pilot, Watchdog, Vigil, or ground command.

### Vigil

The Vigil is an evidence layer with no command authority. It estimates drift in inter-layer independence using baseline-referenced residual dependence, controlled sentinel tests where safe, and explicit uncertainty intervals. Vigil evidence may reduce authority but cannot promote it by itself.

## 2. Failure-Cause Overlap Index

For failure class `k`, let `M[i,k]` be the family of minimal cut sets sufficient to defeat layer `i` with respect to its stated safety function.

### 2.1 Structural FCOI

For layers `i` and `j`:

```text
FCOI_S(i,j,k) = |M[i,k] ∩ M[j,k]| / |M[i,k] ∪ M[j,k]|
```

The structural form ranges from 0 to 1. It is a property of the causal model, not a claim of ground truth. Exact-match Jaccard can understate similarity when two cut sets share nearly all root causes but differ by one event; therefore it is a screening instrument and must be accompanied by a near-match census or weighted-incidence refinement.

### 2.2 Probabilistic FCOI

Let `F[i,k]` denote failure of layer `i` in class `k` during exposure interval `T`, and let `G[i,j,k]` denote the event that both failures propagate through at least one shared modeled root cause. Then:

```text
FCOI_P(i,j,k,T) = P(F[i,k] ∩ F[j,k] ∩ G[i,j,k] | evidence_T)
                  ------------------------------------------------
                  P(F[i,k] ∪ F[j,k] | evidence_T)
```

Root-cause occurrence rates come from environment models and heritage data; propagation parameters come from test, analysis, and FMEA. Every estimate carries an uncertainty or sensitivity interval. A point estimate without its interval is not a valid operational report.

### 2.3 Conservative runtime value

For budgeting, CERBERUS uses the upper defensible bound:

```text
FCOI_bar(i,j,k,t) = upper_bound(FCOI_P(i,j,k,t))
```

Higher overlap means less independence, so using the lower bound would flatter the system.

## 3. Independence budget

For each failure class `k`, design review establishes an acceptable overlap ceiling `theta[k]`.

```text
O[k,t] = max over all layer pairs (i,j) of FCOI_bar(i,j,k,t)
m[k,t] = theta[k] - O[k,t]
b[k,t] = clip(m[k,t] / theta[k], 0, 1)
B[t]   = min over k of b[k,t]
```

`B=1` represents full certified margin and `B=0` means at least one failure class has reached its certified overlap ceiling.

Authority is discretized:

- **A3** — full negotiated Pilot proposal envelope.
- **A2** — restricted proposal magnitudes and stronger consensus requirements.
- **A1** — Watchdog-directed operation; Pilot advisory only.
- **A0** — Anchor authority and minimum survivable action set.

Demotion is immediate and may skip levels. Promotion is sequential, rate-limited, requires a higher hysteresis threshold than demotion, and requires continuous margin evidence for dwell time `tau`. Ground may veto promotion but is not required for demotion.

## 4. Common stimulus versus common cause

Channels exposed to the same sky, thermal cycle, or radiation environment will correlate. The Vigil therefore conditions on measured common environmental inputs and monitors drift from commissioning baselines rather than absolute correlation.

The current prototype uses simpler residual statistics and sequential change detection. Conditional transfer entropy remains a proposed research extension because it is data-hungry, estimator-sensitive, and vulnerable under non-stationary telemetry.

A passive alarm cannot always distinguish an unmodeled benign stimulus from harmful coupling. CERBERUS treats that ambiguity conservatively: reduce the independence budget, queue active interrogation where safe, and request ground diagnosis.

## 5. Sentinel injection

A sentinel is a bounded, statistically characterized perturbation used to test whether a signal propagates into a channel declared independent.

Channels are classified as:

- **injectable** — bounded, reversible perturbation with hardware amplitude cap, duration limit, maneuver/safing exclusion, and automatic removal;
- **passive-only** — monitored but never perturbed;
- **excluded** — no valid bounded perturbation exists.

A sentinel safety case must show that amplitude remains below a fixed fraction of the characterized noise floor, induced state-estimate error remains below the smallest actuation deadband, and the achieved detection power is documented by an ROC analysis.

## 6. Pilot red team and monotonicity ratchet

During idle mission phases, the Pilot may attack the correlation map in sandboxed shadow mode. It may propose missing shared pathways and test them against simulation or replayed telemetry.

The ratchet is one-directional: a discovered pathway may reduce claimed independence, tighten budgets, or narrow authority. Pilot output can never expand the safety claim or relax a constraint. The dog may find holes in the fence; it may never declare the fence sound.

## 7. Safety is not availability

Loss or inconsistency of the Vigil collapses the independence budget conservatively, but an A0 state must remain recoverable rather than mission-dead.

A0 maintains:

- power-positive attitude;
- thermal survival limits;
- authenticated command contact;
- a diagnostic beacon carrying Vigil state and the margin trace;
- bounded fault isolation;
- an expiring diagnostic-recovery window.

Ground recovery is not an override. An authenticated two-party directive may command diagnostics, re-baselining, and re-arming of the promotion law. Ground cannot write the budget, assign an authority level, bypass dwell evidence, or override Anchor hardware invariants. The authorization expires if fresh in-flight evidence is not produced.

## 8. Shared-ontology limitation

All model-based mechanisms inherit the causal ontology. A coupling mechanism absent from the graph can evade FCOI computation, conditioning, red-team search boundaries, and the stated survival map at once.

CERBERUS therefore proposes a future graph-external empirical witness: a separately implemented, model-light monitor using different representations and assumptions. It may only reduce confidence; it cannot certify independence or promote authority. This does not solve ontology incompleteness, but prevents the causal graph from being the sole judge of its own adequacy.

## 9. Reproducible experiment

The included fixed-seed synthetic experiment tests a narrow claim: after conditioning two channels on a measured common environment, an emerging latent shared pathway can be detected from residual dependence before a predefined behavioral-symptom time.

Supplied results:

- nominal false alarms: **0/200**;
- coupling detections: **200/200**;
- median detection sample: **1061.5**;
- median lead before symptom: **238.5 samples**;
- 10th–90th percentile lead: **160.9–319.6 samples**.

These are properties of the supplied synthetic model only. They do not validate flight performance, full probabilistic FCOI, transfer entropy, sentinel safety, or operational authority control.

## 10. Implementation boundary

### Implemented research artifacts

- browser Vigil Lab demonstrator;
- fixed-seed synthetic independence-decay experiment;
- Adversarial Casebook;
- Anchor Reference Specification;
- illustrative A3–A0 authority-state transitions.

### Specified but not implemented

- exact minimal-cut-set structural FCOI engine;
- operational probabilistic FCOI estimator;
- integrated Pilot shadow-mode red team;
- authenticated expiring ground-recovery command stack.

### Proposed or open

- conditional transfer entropy extension;
- hardware-in-the-loop sentinel safety case;
- graph-external empirical witness;
- conservative three-layer reliability proof;
- flight and hardware-in-the-loop validation.

## 11. Novelty position

CERBERUS does not claim to invent Simplex runtime assurance, common-cause reliability modeling, dynamic watermarking, change-point detection, hysteresis, dwell-time switching, or fault-dependent autonomy restriction.

The candidate contribution is the composition of those foundations into a loop where measured inter-layer failure-mode independence is the controlled runtime resource. Novelty remains a hypothesis subject to continued primary-source and external expert review.

## Conclusion

CERBERUS treats the property on which layered assurance depends—failure-mode independence—as measurable, perishable, attackable, and budgetable. Authority is rented against the pessimistic evidence for that independence; it is never owned.
