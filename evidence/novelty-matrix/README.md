# CERBERUS v3.3 Novelty Matrix

This matrix separates established foundations from the candidate CERBERUS contribution. It is a research-positioning aid, not a patentability opinion and not proof that no obscure prior work exists.

| ID | Candidate claim | Closest established foundation | CERBERUS distinction | Confidence / permitted wording |
|---|---|---|---|---|
| N-01 | Layered untrusted controller plus trusted safety gate | Simplex and runtime-assurance architectures | None by itself | **Established.** CERBERUS builds on Simplex/RTA. |
| N-02 | Minimal deterministic survival layer below the gate | Safety controllers, safing modes, FDIR | Anchor is specified as a mission-survivable authority floor with bounded recovery | **Synthesis.** Do not claim invention of safing. |
| N-03 | Explicit engineering of diverse failure causes across layers | N-version diversity and common-cause reliability | Applies causal-diversity analysis across heterogeneous assurance layers | **Plausibly distinctive application.** |
| N-04 | Structural FCOI over layer minimal-cut-set families | Fault-tree minimal cut sets and Jaccard-style overlap | A named overlap metric for heterogeneous assurance-layer failure mechanisms | **Candidate method contribution; requires external review.** |
| N-05 | Probabilistic FCOI as shared-cause joint failure divided by union failure | Beta/alpha-factor common-cause models and PRA | Generalizes the accounting target from duplicated components to heterogeneous layers | **Candidate formalization; not invention of CCF modeling.** |
| N-06 | Runtime estimate of inter-layer failure-mode overlap | Online health monitoring and adaptive risk estimation | The monitored property is independence of the assurance layers themselves | **Strong candidate distinction.** |
| N-07 | Pessimistic upper FCOI bound directly budgets autonomy authority | Risk-adaptive autonomy and fault-dependent reconfiguration | Authority contracts specifically against measured inter-layer overlap | **Central architectural novelty hypothesis.** |
| N-08 | Immediate demotion, slow evidence-gated promotion | Hysteresis and dwell-time supervisory control | Applies asymmetric restoration to independence-budget authority | **Established controls, distinctive composition.** |
| N-09 | Physical watermarking repurposed to test layer independence | Dynamic watermarking for spoof/replay detection | Sentinel propagation falsifies a declared independence relationship | **Plausibly novel repurposing; continue literature search.** |
| N-10 | Passive conditioning distinguishes shared stimulus from emerging coupling | Partial correlation, residual analysis, change-point detection | Integrated into independence-budget evidence | **Established statistics, architecture-level synthesis.** |
| N-11 | Pilot attacks the correlation map in zero-authority shadow mode | Adversarial testing, falsification, runtime assurance | Uses an adaptive reasoner only as a discovery engine against the safety case | **Distinctive integration.** |
| N-12 | Monotonicity ratchet: adaptive output may only reduce trust | One-way safety interlocks and conservative assurance | Makes an unreliable red team safe by forbidding upward safety claims | **Strong design contribution; formal proof remains open.** |
| N-13 | A0 preserves availability, authenticated contact, and recoverability | Spacecraft safe modes and resilient operations | Explicitly treats safety and availability as co-equal reported outcomes | **Synthesis; do not claim invention of recoverable safe mode.** |
| N-14 | Ground can reopen diagnostics but cannot assign authority | Secure commanding and two-person authorization | Ground is modeled as a failure cause and cannot bypass onboard evidence | **Distinctive assurance policy.** |
| N-15 | Ground recovery authorization expires | Capability expiration and secure command windows | Bounds the damage from compromised or mistaken ground recovery | **Established security concept, distinctive application.** |
| N-16 | Shared causal ontology identified as a common-cause failure | Model uncertainty and epistemic uncertainty literature | Treats ontology dependence as correlation across every assurance mechanism | **Important limitation and research framing.** |
| N-17 | Graph-external empirical witness may only reduce confidence | Independent monitoring and anomaly detection | Adds representation diversity at the epistemic level without permitting certification | **Proposed future work, not implemented.** |
| N-18 | Complete loop: define → monitor → attack → budget → demote → evidence-gated restore | Pieces exist across RTA, CCF, watermarking, FDIR, and adaptive autonomy | Composition makes measured independence the controlled runtime resource | **Best reviewer-safe novelty hypothesis:** no exact match located in the targeted review. |

## Claim discipline

Preferred language:

> CERBERUS proposes an architecture in which the pessimistic estimate of inter-layer failure-mode independence is treated as a perishable runtime resource that constrains authority.

Avoid:

- “No one has ever studied independence at runtime.”
- “CERBERUS invents runtime assurance.”
- “FCOI is a ground-truth probability of safety.”
- “The prototype proves flight readiness.”

## Review status

- Primary-reference metadata and cited use were checked for the retained v3.3 evidence set.
- The review was targeted rather than exhaustive.
- Patentability, freedom to operate, and obscure-prior-art completeness were not evaluated.
- Every novelty claim remains open to narrowing when stronger prior art is found.
