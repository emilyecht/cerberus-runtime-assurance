# CERBERUS Research Roadmap

## Near term

- Reproduce the synthetic Vigil experiment in a clean environment and add automated checks.
- Extend the implemented Boolean structural-FCOI slice with reviewed causal inputs, a separate near-match census and scalability comparisons; see docs/fcoi-engine-v1/boolean-vertical-slice.md.
- Add uncertainty propagation for probabilistic FCOI and pessimistic upper-bound budgeting.
- Convert the A0 Anchor specification into an executable state-machine model.
- Build a graph-external empirical witness to reduce dependence on a shared causal ontology.

## Validation track

- Replace synthetic channels with spacecraft-like telemetry models.
- Evaluate false alarms under non-stationarity, missing data, clock drift, and degrading environment sensors.
- Add hardware-in-the-loop sentinel-injection safety tests.
- Measure authority-state chattering, demotion latency, restoration time, and mission availability.

## Publication track

- Complete an external technical review of the novelty matrix.
- Freeze a citable paper version after reviewer corrections.
- Prepare a bounded experiment proposal for runtime-independence monitoring.
