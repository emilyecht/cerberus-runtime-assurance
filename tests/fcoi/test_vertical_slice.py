# Copyright 2026 Emily Echterhoff
# SPDX-License-Identifier: MIT

"""Hand calculations, independent exhaustive truth tables and strict failures."""

from copy import deepcopy
import hashlib
from importlib.resources import files
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from cerberus_fcoi import EnumerationLimit, ModelError, analyze_model, parse_model

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = json.loads((ROOT / "examples/fcoi/hand-calculated.json").read_text())["cases"]


def truth_table_minimals(model, top):
    """Enumerate all assignments first; no cut-set composition or engine helpers."""
    nodes = {node["id"]: node for node in model["nodes"]}
    variables = sorted(cause["id"] for cause in model["root_causes"])

    def value(node_id, assignment):
        node = nodes[node_id]
        if node["type"] == "basic_event":
            return node["root_cause"] in assignment
        if node["type"] == "constant":
            return node["value"]
        children = [value(child, assignment) for child in node["inputs"]]
        return all(children) if node["type"] == "and_gate" else any(children)

    sufficient = []
    for count in range(len(variables) + 1):
        for assignment in combinations(variables, count):
            assigned = frozenset(assignment)
            if value(top, assigned):
                sufficient.append(assigned)
    minimal = [a for a in sufficient if not any(b < a for b in sufficient)]
    return [sorted(a) for a in sorted(minimal, key=lambda a: (len(a), tuple(sorted(a))))]


class VerticalSliceTests(unittest.TestCase):
    def example(self, index=2):
        return deepcopy(FIXTURES[index]["model"])

    def test_all_hand_calculated_families_and_exact_overlaps(self):
        for fixture in FIXTURES:
            with self.subTest(fixture["name"]):
                report = analyze_model(fixture["model"])
                for layer, expected in fixture["expected"].items():
                    self.assertEqual(report["layers"][layer]["minimal_cut_sets"], expected)
                self.assertEqual(report["pairs"][0]["exact_structural_fcoi"], fixture["ratio"])
                if "shared" in fixture:
                    self.assertEqual(report["pairs"][0]["shared_root_causes"], fixture["shared"])

    def test_all_hand_fixtures_against_independent_truth_tables(self):
        for fixture in FIXTURES:
            for layer, top in fixture["model"]["top_events"].items():
                with self.subTest(fixture=fixture["name"], layer=layer):
                    self.assertEqual(truth_table_minimals(fixture["model"], top), fixture["expected"][layer])

    def test_seeded_small_dags_against_independent_truth_tables(self):
        rng = random.Random(731)
        for example in range(60):
            model = self.example(1)
            for index in range(6):
                prior = [node["id"] for node in model["nodes"]]
                model["nodes"].append({"id": f"gate{index}", "type": rng.choice(["and_gate", "or_gate"]),
                                       "inputs": rng.choices(prior, k=rng.randint(1, 3)), "mechanism_refs": []})
            model["top_events"] = {"Pilot": "gate5", "Watchdog": "gate4"}
            report = analyze_model(model)
            for layer, top in model["top_events"].items():
                with self.subTest(example=example, layer=layer):
                    self.assertEqual(report["layers"][layer]["minimal_cut_sets"], truth_table_minimals(model, top))

    def test_permutations_do_not_change_report_or_normalized_hash(self):
        model = self.example()
        expected = analyze_model(model)
        model["nodes"].reverse()
        model["root_causes"].reverse()
        model["top_events"] = dict(reversed(list(model["top_events"].items())))
        for node in model["nodes"]:
            if "inputs" in node:
                node["inputs"].reverse()
        self.assertEqual(analyze_model(model), expected)

    def test_node_renaming_preserves_families_and_metrics(self):
        model = self.example(3)
        old = analyze_model(model)
        for node in model["nodes"]:
            node["id"] = "renamed-" + node["id"]
            if "inputs" in node:
                node["inputs"] = ["renamed-" + child for child in node["inputs"]]
        model["top_events"] = {k: "renamed-" + v for k, v in model["top_events"].items()}
        new = analyze_model(model)
        self.assertEqual(new["pairs"], old["pairs"])
        for layer in old["layers"]:
            self.assertEqual(new["layers"][layer]["minimal_cut_sets"], old["layers"][layer]["minimal_cut_sets"])

    def test_undeveloped_or_incomplete_never_becomes_numeric_zero(self):
        for field, value in (("undeveloped_events", ["unknown shared power path"]), ("evidence_status", "incomplete")):
            model = self.example()
            model[field] = value
            report = analyze_model(model)
            self.assertIsNone(report["pairs"][0]["exact_structural_fcoi"])
            self.assertEqual(report["pairs"][0]["status"], "not_estimable")
            self.assertIsNone(report["layers"]["Pilot"]["minimal_cut_sets"])
            self.assertEqual(report[field], value)

    def test_empty_family_differs_from_empty_cut_set(self):
        empty = analyze_model(FIXTURES[8]["model"])
        self.assertIsNone(empty["pairs"][0]["exact_structural_fcoi"])
        self.assertEqual(empty["pairs"][0]["union_count"], 0)
        unconditional = analyze_model(FIXTURES[9]["model"])
        self.assertEqual(unconditional["layers"]["Pilot"]["minimal_cut_sets"], [[]])
        self.assertTrue(unconditional["layers"]["Pilot"]["unconditional_failure"])

    def test_invalid_models_fail_instead_of_returning_a_score(self):
        invalid = []
        model = self.example(); model["top_events"]["Pilot"] = "missing"; invalid.append(model)
        model = self.example(); model["nodes"][0]["root_cause"] = "missing"; invalid.append(model)
        model = self.example(); model["nodes"].append(deepcopy(model["nodes"][0])); invalid.append(model)
        model = self.example(); model["root_causes"].append(deepcopy(model["root_causes"][0])); invalid.append(model)
        model = self.example(); model["nodes"][-1]["inputs"] = ["missing"]; invalid.append(model)
        model = self.example(); model["nodes"][-1]["type"] = "not_gate"; invalid.append(model)
        model = self.example(); model["probability"] = 0.5; invalid.append(model)
        model = self.example(); model["schema_version"] = "0.0.0"; invalid.append(model)
        model = self.example(); model["nodes"][-1]["inputs"] = []; invalid.append(model)
        model = self.example(); model["nodes"].append({"id":"unreachable-cycle", "type":"and_gate", "inputs":["unreachable-cycle"], "mechanism_refs":[]}); invalid.append(model)
        for number, model in enumerate(invalid):
            with self.subTest(number=number), self.assertRaises(ModelError):
                analyze_model(model)

    def test_duplicate_json_keys_and_nonfinite_values_are_rejected(self):
        for text in ('{"id": 1, "id": 2}', '{"nested": {"id":1,"id":2}}', '{"value":NaN}', '{"value":Infinity}'):
            with self.subTest(text=text), self.assertRaises(ModelError):
                parse_model(text)

    def test_no_partial_results_when_exact_enumeration_exceeds_budgets(self):
        with self.assertRaises(EnumerationLimit):
            analyze_model(self.example(), max_cut_sets=1)
        with self.assertRaises(EnumerationLimit):
            analyze_model(self.example(), max_candidates=1)
        with self.assertRaises(ModelError):
            analyze_model(self.example(), max_cut_sets=True)

    def test_input_model_is_not_mutated(self):
        model = self.example()
        before = deepcopy(model)
        analyze_model(model)
        self.assertEqual(model, before)

    def test_schema_is_frozen_to_recorded_bytes(self):
        actual = hashlib.sha256(files("cerberus_fcoi").joinpath("model-v1.schema.json").read_bytes()).hexdigest()
        expected = (ROOT / "schemas/fcoi-model-v1.sha256").read_text().split()[0]
        self.assertEqual(actual, expected)

    def test_cli_roundtrip_determinism_and_invalid_input_exit(self):
        example = ROOT / "examples/fcoi/partial-overlap.json"
        command = [sys.executable, "-m", "cerberus_fcoi", str(example)]
        first = subprocess.run(command, text=True, capture_output=True, check=True)
        second = subprocess.run(command, text=True, capture_output=True, check=True)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout)["pairs"][0]["exact_structural_fcoi"], 1/3)
        with TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"schema_version":"invalid"}')
            failed = subprocess.run([sys.executable, "-m", "cerberus_fcoi", str(path)], text=True, capture_output=True)
            self.assertEqual(failed.returncode, 2)
            self.assertEqual(failed.stdout, "")
            self.assertIn("No result", failed.stderr)


if __name__ == "__main__":
    unittest.main()
