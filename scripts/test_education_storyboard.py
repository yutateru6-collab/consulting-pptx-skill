#!/usr/bin/env python3
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check_education_storyboard import validate  # noqa: E402

EXAMPLE = HERE.parent / "templates" / "education-storyboard.example.json"


class EducationStoryboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_example_passes(self):
        report = validate(deepcopy(self.base))
        self.assertEqual(report.fail_count, 0, [i.message for i in report.issues])

    def test_visible_answer_fails(self):
        data = deepcopy(self.base)
        data["slides"][4]["answerInitiallyVisible"] = True
        report = validate(data)
        self.assertTrue(any(i.code == "ANSWER_VISIBLE" and i.severity == "FAIL" for i in report.issues))

    def test_prerequisite_order_fails(self):
        data = deepcopy(self.base)
        data["slides"][1]["teaches"] = ["tense-choice"]
        data["slides"][2]["teaches"] = ["present-perfect-link"]
        report = validate(data)
        self.assertTrue(any(i.code == "PREREQUISITE_ORDER" for i in report.issues))

    def test_objective_needs_evidence(self):
        data = deepcopy(self.base)
        for slide in data["slides"]:
            if slide["role"] in {"retrieval", "guided-practice", "independent-practice", "exit-ticket", "quiz"}:
                slide["objectiveIds"] = [oid for oid in slide.get("objectiveIds", []) if oid != "obj-choose"]
        report = validate(data)
        self.assertTrue(any(i.code == "OBJECTIVE_UNCHECKED" and i.objective_id == "obj-choose" for i in report.issues))


if __name__ == "__main__":
    unittest.main()
