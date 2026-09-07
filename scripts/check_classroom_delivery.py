#!/usr/bin/env python3
"""Final delivery gate for classroom PPTX QA artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--machine", type=Path, required=True)
    ap.add_argument("--visual", type=Path, required=True)
    args = ap.parse_args()

    errors: list[str] = []

    try:
        machine = load_json(args.machine)
    except Exception as e:
        print(f"FAIL: cannot read machine QA JSON: {e}")
        return 2

    try:
        visual = load_json(args.visual)
    except Exception as e:
        print(f"FAIL: cannot read visual QA JSON: {e}")
        return 2

    if int(machine.get("fail_count", 999999)) != 0:
        errors.append(f"machine QA has FAIL={machine.get('fail_count')}")

    if visual.get("overall_status") != "PASS":
        errors.append(f"visual QA status is {visual.get('overall_status')!r}, expected 'PASS'")

    if visual.get("reviewed_all_slides") is not True:
        errors.append("visual QA did not confirm all slides were reviewed")

    if visual.get("reviewed_contact_sheet") is not True:
        errors.append("visual QA did not confirm contact-sheet review")

    expected = visual.get("slides_expected")
    reviewed = visual.get("slides_reviewed")
    if not isinstance(expected, int) or not isinstance(reviewed, int) or reviewed != expected:
        errors.append(f"visual QA slide coverage mismatch: reviewed={reviewed}, expected={expected}")

    if int(visual.get("unresolved_high", 999999)) != 0:
        errors.append(f"visual QA has unresolved_high={visual.get('unresolved_high')}")

    if int(visual.get("unresolved_medium", 999999)) != 0:
        errors.append(f"visual QA has unresolved_medium={visual.get('unresolved_medium')}")

    if visual.get("fixes_made") is True and visual.get("rerendered_after_fixes") is not True:
        errors.append("fixes were made but rerendered_after_fixes is not true")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"CLASSROOM_DELIVERY: FAIL ({len(errors)} issue(s))")
        return 1

    print("CLASSROOM_DELIVERY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
