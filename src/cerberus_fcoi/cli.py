# Copyright 2026 Emily Echterhoff
# SPDX-License-Identifier: MIT

"""Read-only local model CLI. Errors never produce a numeric overlap report."""

import argparse
import json
from pathlib import Path
import sys

from .engine import ModelError, analyze_model, parse_model


def main():
    parser = argparse.ArgumentParser(description="CERBERUS design-time structural FCOI slice; no runtime authority")
    parser.add_argument("model", type=Path)
    args = parser.parse_args()
    try:
        report = analyze_model(parse_model(args.model.read_text(encoding="utf-8")))
    except (ModelError, OSError) as exc:
        print(f"No result: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, indent=2, allow_nan=False))
    return 0
