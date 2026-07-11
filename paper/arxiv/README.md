# CERBERUS v3.5 arXiv source

This directory contains the submission-ready source for:

**CERBERUS: Runtime Independence Budgeting for Layered Assurance in Autonomous Systems**

## Build

```bash
latexmk -pdf -interaction=nonstopmode CERBERUS_v3.5_arXiv.tex
```

The manuscript uses only local text assets: the LaTeX source, section files, exact verified bibliography files, and a downsampled CSV plotted with PGFPlots.

## Evidence boundary

The paper is a research preprint, not flight-certified software, a completed safety case, or a claim of operational readiness. The fixed-seed experiment is explicitly framed as matched-model pipeline verification.

## Suggested arXiv routing

Likely primary categories are `cs.SY` or `eess.SY`, with `cs.RO` as a possible cross-list. The submitter should select the category that best matches the final emphasis and endorsement availability.

## Repositories

- Architecture and paper: https://github.com/k766807/cerberus-runtime-assurance
- Reproducible experiment: https://github.com/k766807/cerberus-vigil-experiment
