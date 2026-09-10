#!/usr/bin/env python3
"""Smoke tests for classroom English line-balance heuristics."""
from __future__ import annotations

from check_classroom_english_balance import explicit_balance_issue


def main() -> int:
    good = "If I had known her address,\nI would have written to her."
    sev, reason = explicit_balance_issue(good)
    assert sev != "FAIL", (sev, reason)

    bad_orphan = "If I\nwere you, I would tell the truth."
    sev, reason = explicit_balance_issue(bad_orphan)
    assert sev == "FAIL", (sev, reason)
    assert "orphan" in reason.lower() or "uneven" in reason.lower()

    bad_function_word = "I want to\nstudy English abroad next year."
    sev, reason = explicit_balance_issue(bad_function_word)
    assert sev == "FAIL", (sev, reason)
    assert "function word" in reason.lower()

    balanced = "If it rains tomorrow,\nI will stay home."
    sev, reason = explicit_balance_issue(balanced)
    assert sev != "FAIL", (sev, reason)

    print("CLASSROOM_ENGLISH_BALANCE_SMOKE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
