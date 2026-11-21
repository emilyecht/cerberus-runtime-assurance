# Structural FCOI evaluation fixtures version 1

The Boolean schema 1.0.0, recorded schema hash and deterministic minimal-cut-set
algorithm were already implemented on main at
`48e62fd8a645c10c9161dadf62c07d0eb1c2ee5a`. This evaluation round retains those
semantics and the ten original hand-calculated fixtures. It adds a three-layer
authority-boundary example and malformed-Unicode refusal checks.

## Three layer hand calculation

`examples/fcoi/authority-boundary.json` is an explicitly unreviewed hypothetical
fault model. It is not a measured fault model of CERBERUS Cyber.

| Layer | Minimal sufficient root-cause sets |
| --- | --- |
| Guardian | {GuardianVerifier}, {SharedStore} |
| Kernel | {KernelVerifier}, {SharedStore} |
| Controller | {ControllerKey}, {GuardianVerifier, KernelVerifier} |

Guardian and Kernel have one identical minimal set in a union of three, giving
exact structural overlap 1/3. Controller has zero identical sets with either
other layer while sharing a verifier cause with each. This demonstrates why zero
exact overlap must never be read as causal or operational independence.

Regression checks independently enumerate all 16 assignments of the four causes
for each of three tops, compare them to the hand results, and verify byte-identical
CLI output under four Python hash seeds. The existing ten calculations, 60 seeded
small DAGs, incomplete-evidence suppression and no-partial-result budgets remain
in the suite. Invalid UTF-8 files and escaped unpaired Unicode surrogates now
produce a controlled error with no report, rather than an uncaught traceback.
Valid model outputs and their normalized hashes are unchanged.

## Reproduce

```sh
python -m pip install .
python -m unittest discover -s tests/fcoi -v
python -m cerberus_fcoi examples/fcoi/authority-boundary.json
```

The baseline main suite has 13 test methods; the expanded suite has 16. A method
may exercise many fixtures and subcases, so these are not independent security
trials. No live authority, operational enforcement, probabilistic FCOI, causal
discovery or formal verification is added. CERBERUS remains TRL 2-3 research.

## Possible later use by Cyber

An evaluator could construct a separate, reviewed model of shared storage,
controller keys, policy provenance, time and revocation delivery, then apply this
standalone analyzer to that model. Each sufficient-failure assumption would need
evidence or a declared undeveloped event. Such a model could prioritize Cyber
tests; it would not grant execution authority or transfer a Protocol score into
Cyber evidence. There is no runtime or package dependency between the projects.
