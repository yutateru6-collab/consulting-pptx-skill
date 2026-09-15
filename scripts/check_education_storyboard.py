#!/usr/bin/env python3
"""Validate an Education Mode storyboard before classroom slide generation.

The checker intentionally validates pedagogy and sequencing rather than visual layout.
Visual/PPTX QA remains the responsibility of the existing classroom checkers.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

CHECK_ROLES = {"retrieval", "guided-practice", "independent-practice", "exit-ticket", "quiz"}
EXAMPLE_ROLES = {"example", "worked-example", "guided-practice"}
FORMAL_ROLES = {"rule", "definition", "concept"}
MOTIVATION_ROLES = {"hook", "noticing", "compare", "example", "problem"}
CONTENT_ROLES = {
    "hook", "objective", "retrieval", "noticing", "rule", "definition", "concept",
    "example", "worked-example", "compare", "misconception", "guided-practice",
    "independent-practice", "recap", "exit-ticket", "quiz", "section", "cover",
}
PRACTICE_ROLES = {"retrieval", "guided-practice", "independent-practice", "exit-ticket", "quiz"}
VALID_BLOOM = {"remember", "understand", "apply", "analyze", "evaluate", "create"}
VAGUE_OBJECTIVE_PHRASES = {"understand", "know", "learn", "be familiar with"}


@dataclass
class Issue:
    severity: str  # FAIL | WARN
    code: str
    message: str
    slide_id: Optional[str] = None
    objective_id: Optional[str] = None
    concept_id: Optional[str] = None


class Report:
    def __init__(self) -> None:
        self.issues: List[Issue] = []

    def fail(self, code: str, message: str, **kwargs: Any) -> None:
        self.issues.append(Issue("FAIL", code, message, **kwargs))

    def warn(self, code: str, message: str, **kwargs: Any) -> None:
        self.issues.append(Issue("WARN", code, message, **kwargs))

    @property
    def fail_count(self) -> int:
        return sum(i.severity == "FAIL" for i in self.issues)

    @property
    def warn_count(self) -> int:
        return sum(i.severity == "WARN" for i in self.issues)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": "PASS" if self.fail_count == 0 else "FAIL",
            "failCount": self.fail_count,
            "warnCount": self.warn_count,
            "issues": [asdict(i) for i in self.issues],
        }


def _ids(items: Iterable[Dict[str, Any]]) -> List[str]:
    return [str(x.get("id", "")).strip() for x in items]


def _duplicates(values: Iterable[str]) -> Set[str]:
    seen: Set[str] = set()
    dup: Set[str] = set()
    for v in values:
        if not v:
            continue
        if v in seen:
            dup.add(v)
        seen.add(v)
    return dup


def _string_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x) for x in value]
    return [str(value)]


def _validate_concept_graph(concepts: List[Dict[str, Any]], report: Report) -> Dict[str, Dict[str, Any]]:
    concept_map: Dict[str, Dict[str, Any]] = {}
    for c in concepts:
        cid = str(c.get("id", "")).strip()
        if not cid:
            report.fail("CONCEPT_ID_MISSING", "Every concept needs a non-empty id.")
            continue
        if cid in concept_map:
            report.fail("CONCEPT_ID_DUPLICATE", f"Duplicate concept id: {cid}", concept_id=cid)
            continue
        concept_map[cid] = c

    for cid, c in concept_map.items():
        for prereq in _string_list(c.get("prerequisites")):
            if prereq not in concept_map:
                report.fail(
                    "PREREQUISITE_UNKNOWN",
                    f"Concept '{cid}' references unknown prerequisite '{prereq}'.",
                    concept_id=cid,
                )

    state: Dict[str, int] = {cid: 0 for cid in concept_map}

    def visit(cid: str, stack: List[str]) -> None:
        if state[cid] == 1:
            cycle = " -> ".join(stack + [cid])
            report.fail("PREREQUISITE_CYCLE", f"Concept prerequisite cycle detected: {cycle}", concept_id=cid)
            return
        if state[cid] == 2:
            return
        state[cid] = 1
        for prereq in _string_list(concept_map[cid].get("prerequisites")):
            if prereq in concept_map:
                visit(prereq, stack + [cid])
        state[cid] = 2

    for cid in concept_map:
        if state[cid] == 0:
            visit(cid, [])
    return concept_map


def validate(data: Dict[str, Any]) -> Report:
    report = Report()
    meta = data.get("meta") or {}
    objectives = data.get("objectives") or []
    concepts = data.get("concepts") or []
    slides = data.get("slides") or []

    if not isinstance(meta, dict):
        report.fail("META_INVALID", "meta must be an object.")
        meta = {}
    if str(meta.get("mode", "")).lower() != "education":
        report.fail("MODE_NOT_EDUCATION", "meta.mode must be 'education'.")
    for field in ("audience", "goal"):
        if not str(meta.get(field, "")).strip():
            report.fail("META_REQUIRED", f"meta.{field} is required.")

    if not isinstance(objectives, list) or not objectives:
        report.fail("OBJECTIVES_MISSING", "At least one learning objective is required.")
        objectives = []
    if not isinstance(concepts, list):
        report.fail("CONCEPTS_INVALID", "concepts must be an array.")
        concepts = []
    if not isinstance(slides, list) or not slides:
        report.fail("SLIDES_MISSING", "At least one slide is required.")
        slides = []

    objective_ids = _ids(objectives)
    for dup in _duplicates(objective_ids):
        report.fail("OBJECTIVE_ID_DUPLICATE", f"Duplicate objective id: {dup}", objective_id=dup)
    objective_map = {str(o.get("id", "")).strip(): o for o in objectives if str(o.get("id", "")).strip()}
    for o in objectives:
        oid = str(o.get("id", "")).strip()
        if not oid:
            report.fail("OBJECTIVE_ID_MISSING", "Every objective needs a non-empty id.")
            continue
        text = str(o.get("text", "")).strip()
        if not text:
            report.fail("OBJECTIVE_TEXT_MISSING", "Objective text is required.", objective_id=oid)
        bloom = str(o.get("bloom", "")).lower().strip()
        if bloom not in VALID_BLOOM:
            report.fail("BLOOM_INVALID", f"Objective '{oid}' has invalid bloom level '{bloom}'.", objective_id=oid)
        lower = text.lower()
        if any(lower.startswith(p + " ") or lower == p for p in VAGUE_OBJECTIVE_PHRASES):
            report.warn(
                "OBJECTIVE_VAGUE_VERB",
                f"Objective '{oid}' begins with a vague verb; prefer observable evidence (explain/use/compare/justify/etc.).",
                objective_id=oid,
            )

    concept_map = _validate_concept_graph(concepts, report)

    slide_ids = _ids(slides)
    for dup in _duplicates(slide_ids):
        report.fail("SLIDE_ID_DUPLICATE", f"Duplicate slide id: {dup}", slide_id=dup)

    first_teach: Dict[str, Tuple[int, str]] = {}
    slides_by_objective: Dict[str, List[Tuple[int, Dict[str, Any]]]] = {oid: [] for oid in objective_map}
    checks_by_objective: Dict[str, List[Tuple[int, Dict[str, Any]]]] = {oid: [] for oid in objective_map}

    first_formal_idx: Optional[int] = None
    motivation_seen = False

    for idx, slide in enumerate(slides):
        sid = str(slide.get("id", "")).strip() or f"index-{idx+1}"
        role = str(slide.get("role", "")).strip().lower()
        if role not in CONTENT_ROLES:
            report.warn("ROLE_UNKNOWN", f"Slide '{sid}' has unrecognized role '{role}'.", slide_id=sid)
        if role in MOTIVATION_ROLES:
            motivation_seen = True
        if role in FORMAL_ROLES and first_formal_idx is None:
            first_formal_idx = idx
            if not motivation_seen:
                report.warn(
                    "FORMALISM_BEFORE_MOTIVATION",
                    f"First formal explanation appears on '{sid}' before a hook/noticing/example/compare beat.",
                    slide_id=sid,
                )

        title = str(slide.get("title", "")).strip()
        if role not in {"cover", "section"} and not title:
            report.fail("SLIDE_TITLE_MISSING", f"Slide '{sid}' needs a title/action title.", slide_id=sid)

        objective_refs = _string_list(slide.get("objectiveIds"))
        for oid in objective_refs:
            if oid not in objective_map:
                report.fail("OBJECTIVE_REF_UNKNOWN", f"Slide '{sid}' references unknown objective '{oid}'.", slide_id=sid)
            else:
                slides_by_objective[oid].append((idx, slide))
                if role in CHECK_ROLES:
                    checks_by_objective[oid].append((idx, slide))

        if role not in {"cover", "section"} and objective_map and not objective_refs:
            report.warn("SLIDE_NOT_MAPPED", f"Slide '{sid}' is not mapped to a learning objective.", slide_id=sid)

        teaches = _string_list(slide.get("teaches"))
        for cid in teaches:
            if cid not in concept_map:
                report.fail("CONCEPT_REF_UNKNOWN", f"Slide '{sid}' teaches unknown concept '{cid}'.", slide_id=sid, concept_id=cid)
                continue
            first_teach.setdefault(cid, (idx, sid))

        if role in PRACTICE_ROLES and slide.get("answerInitiallyVisible") is not False:
            report.fail(
                "ANSWER_VISIBLE",
                f"Practice/check slide '{sid}' must set answerInitiallyVisible=false.",
                slide_id=sid,
            )

        builds = slide.get("builds")
        if role not in {"cover", "section"}:
            if not isinstance(builds, list) or len(builds) == 0:
                report.warn("BUILDS_MISSING", f"Slide '{sid}' has no staged builds declared.", slide_id=sid)
            elif len(builds) > 6:
                report.warn("TOO_MANY_BUILDS", f"Slide '{sid}' has {len(builds)} builds; consider splitting after 6.", slide_id=sid)

        notes = slide.get("notes") or {}
        if role not in {"cover", "section"}:
            if not isinstance(notes, dict) or not any(str(notes.get(k, "")).strip() for k in ("explanation", "teacherPrompt", "expectedAnswer", "clickOrder")):
                report.fail("NOTES_MISSING", f"Slide '{sid}' needs substantive teacher notes.", slide_id=sid)

    # Prerequisite ordering and missing teaching slides.
    for cid, concept in concept_map.items():
        if bool(concept.get("assumed")):
            continue
        if cid not in first_teach:
            report.fail("CONCEPT_NEVER_TAUGHT", f"Concept '{cid}' is not marked assumed and is never taught.", concept_id=cid)
            continue
        cidx, csid = first_teach[cid]
        for prereq in _string_list(concept.get("prerequisites")):
            prereq_obj = concept_map.get(prereq, {})
            if bool(prereq_obj.get("assumed")):
                continue
            if prereq not in first_teach:
                continue
            pidx, psid = first_teach[prereq]
            if pidx >= cidx:
                report.fail(
                    "PREREQUISITE_ORDER",
                    f"Concept '{cid}' is taught on '{csid}' before prerequisite '{prereq}' on '{psid}'.",
                    slide_id=csid,
                    concept_id=cid,
                )

    # Objective coverage and evidence.
    for oid in objective_map:
        if not slides_by_objective.get(oid):
            report.fail("OBJECTIVE_UNCOVERED", f"Objective '{oid}' is not covered by any slide.", objective_id=oid)
        if not checks_by_objective.get(oid):
            report.fail("OBJECTIVE_UNCHECKED", f"Objective '{oid}' has no retrieval/practice/exit-ticket evidence slide.", objective_id=oid)

    # Rule/definition -> example within next 2 slides.
    for idx, slide in enumerate(slides):
        role = str(slide.get("role", "")).strip().lower()
        if role not in FORMAL_ROLES:
            continue
        sid = str(slide.get("id", "")).strip() or f"index-{idx+1}"
        taught = set(_string_list(slide.get("teaches")))
        objectives_here = set(_string_list(slide.get("objectiveIds")))
        found = False
        for next_slide in slides[idx + 1 : idx + 3]:
            next_role = str(next_slide.get("role", "")).strip().lower()
            if next_role not in EXAMPLE_ROLES:
                continue
            next_taught = set(_string_list(next_slide.get("teaches")))
            next_objectives = set(_string_list(next_slide.get("objectiveIds")))
            if (taught and taught & next_taught) or (objectives_here and objectives_here & next_objectives) or (not taught and not objectives_here):
                found = True
                break
        if not found:
            report.fail(
                "EXAMPLE_TOO_FAR",
                f"Formal explanation on '{sid}' needs a concrete/worked example within the next 2 slides.",
                slide_id=sid,
            )

    if slides and not any(str(s.get("role", "")).lower() in {"retrieval", "exit-ticket"} for s in slides):
        report.fail("RETRIEVAL_MISSING", "Deck needs at least one retrieval or exit-ticket slide.")

    if concepts:
        for cid in concept_map:
            if bool(concept_map[cid].get("assumed")) or cid not in first_teach:
                continue
            t_idx, _ = first_teach[cid]
            later_checks = [
                s for s in slides[t_idx + 1 :]
                if str(s.get("role", "")).lower() in CHECK_ROLES and cid in set(_string_list(s.get("checks")) + _string_list(s.get("teaches")))
            ]
            if not later_checks:
                report.warn("CONCEPT_NOT_RETRIEVED", f"Concept '{cid}' is taught but never explicitly checked later.", concept_id=cid)

    output_targets = {x.lower() for x in _string_list(meta.get("outputTargets"))}
    if "google-slides" in output_targets:
        mode = str(meta.get("googleSlidesBuildMode", "")).strip().lower()
        if mode not in {"duplicate-slides", "static", "import-pptx"}:
            report.fail(
                "GOOGLE_SLIDES_BUILD_MODE",
                "When outputTargets includes google-slides, meta.googleSlidesBuildMode must be duplicate-slides, static, or import-pptx.",
            )
        if mode == "duplicate-slides":
            report.warn(
                "GOOGLE_SLIDES_DUPLICATE_BUILD",
                "Google Slides build states should be emitted as duplicate progressive slides; do not claim PowerPoint on-click parity.",
            )

    return report


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an Education Mode storyboard JSON.")
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--json", dest="json_out", type=Path, help="Write machine-readable report JSON.")
    parser.add_argument("--strict-warnings", action="store_true", help="Return non-zero when WARNs exist.")
    args = parser.parse_args(argv)

    try:
        data = json.loads(args.storyboard.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL JSON_READ: {exc}")
        return 2

    report = validate(data)
    payload = report.to_dict()
    if args.json_out:
        args.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for issue in report.issues:
        loc = f" [{issue.slide_id}]" if issue.slide_id else ""
        print(f"{issue.severity} {issue.code}{loc}: {issue.message}")
    print(f"{payload['status']} education-storyboard: FAIL={report.fail_count} WARN={report.warn_count}")

    if report.fail_count:
        return 1
    if args.strict_warnings and report.warn_count:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
