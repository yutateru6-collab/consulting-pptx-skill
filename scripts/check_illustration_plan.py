#!/usr/bin/env python3
"""Validate Illustration Mode planning JSON before slide production.

Usage:
    python3 scripts/check_illustration_plan.py illustration-plan.json
    python3 scripts/check_illustration_plan.py illustration-plan.json --json qa.json
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

ALLOWED_DECISIONS = {"use", "omit"}
ALLOWED_ROLES = {
    "scene",
    "comparison",
    "concept-metaphor",
    "timeline-context",
    "process",
    "mascot-cue",
    "icon-support",
    "diagram-support",
}
ALLOWED_FUNCTIONS = {
    "concretize",
    "contrast",
    "sequence",
    "orient",
    "motivate",
    "signal",
    "retrieve",
}
ALLOWED_LAYOUTS = {
    "text-left-visual-right",
    "visual-left-text-right",
    "paired-scenes",
    "scene-plus-takeaway",
    "margin-mascot",
    "micro-icon-support",
}
ALLOWED_SOURCE_KINDS = {"generated", "external", "local-owned"}
PLACEHOLDER_TOKENS = ("TODO", "TBD", "PLACEHOLDER", "example.com", "ここに")


def _box_ok(box: Any) -> bool:
    if not isinstance(box, dict):
        return False
    try:
        x = float(box["x"])
        y = float(box["y"])
        w = float(box["w"])
        h = float(box["h"])
    except (KeyError, TypeError, ValueError):
        return False
    if not all(math.isfinite(v) for v in (x, y, w, h)):
        return False
    return x >= 0 and y >= 0 and w > 0 and h > 0 and x + w <= 1.0001 and y + h <= 1.0001


def _area(box: dict[str, Any]) -> float:
    return float(box["w"]) * float(box["h"])


def _intersection(a: dict[str, Any], b: dict[str, Any]) -> float:
    ax1, ay1 = float(a["x"]), float(a["y"])
    ax2, ay2 = ax1 + float(a["w"]), ay1 + float(a["h"])
    bx1, by1 = float(b["x"]), float(b["y"])
    bx2, by2 = bx1 + float(b["w"]), by1 + float(b["h"])
    w = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    h = max(0.0, min(ay2, by2) - max(ay1, by1))
    return w * h


def _has_placeholder(value: Any) -> bool:
    text = json.dumps(value, ensure_ascii=False).upper()
    return any(token.upper() in text for token in PLACEHOLDER_TOKENS)


def validate_plan(data: dict[str, Any]) -> dict[str, Any]:
    fails: list[str] = []
    warns: list[str] = []

    if not isinstance(data, dict):
        return {
            "fail_count": 1,
            "warn_count": 0,
            "fails": ["root must be a JSON object"],
            "warnings": [],
        }

    meta = data.get("meta")
    if not isinstance(meta, dict):
        fails.append("meta: missing object")
        meta = {}

    default_style = str(meta.get("defaultStyleFamily") or "").strip()
    if not default_style:
        fails.append("meta.defaultStyleFamily: required")

    output_target = str(meta.get("outputTarget") or "").strip().lower()
    if output_target not in {"pptx", "google-slides", "both"}:
        fails.append("meta.outputTarget: expected pptx, google-slides, or both")

    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        fails.append("slides: must be a non-empty array")
        slides = []

    seen_ids: set[str] = set()
    used_count = 0
    content_like_count = 0
    hero_count = 0
    style_counts: dict[str, int] = {}
    consecutive_layouts: list[tuple[str, str]] = []

    for idx, slide in enumerate(slides, start=1):
        prefix = f"slides[{idx}]"
        if not isinstance(slide, dict):
            fails.append(f"{prefix}: must be an object")
            continue

        sid = str(slide.get("slideId") or "").strip()
        if not sid:
            fails.append(f"{prefix}.slideId: required")
            sid = f"#{idx}"
        elif sid in seen_ids:
            fails.append(f"{prefix}.slideId: duplicate id {sid!r}")
        seen_ids.add(sid)

        slide_type = str(slide.get("slideType") or "content").strip().lower()
        if slide_type not in {"cover", "content", "practice", "summary", "section"}:
            warns.append(f"{sid}: unknown slideType {slide_type!r}; treat as content")
        if slide_type != "cover":
            content_like_count += 1

        decision = str(slide.get("decision") or "").strip().lower()
        if decision not in ALLOWED_DECISIONS:
            fails.append(f"{sid}: decision must be 'use' or 'omit'")
            continue

        reason = str(slide.get("reason") or "").strip()
        if len(reason) < 8:
            fails.append(f"{sid}: reason must explain the teaching/layout decision, not just name it")

        if decision == "omit":
            # Omitted slides should not carry half-filled production fields.
            noisy = [k for k in ("bbox", "prompt", "assetType", "role") if k in slide]
            if noisy:
                warns.append(f"{sid}: decision=omit but production fields remain: {', '.join(noisy)}")
            continue

        used_count += 1

        role = str(slide.get("role") or "").strip()
        if role not in ALLOWED_ROLES:
            fails.append(f"{sid}: role must be one of {sorted(ALLOWED_ROLES)}")

        function = str(slide.get("learningFunction") or "").strip()
        if function not in ALLOWED_FUNCTIONS:
            fails.append(f"{sid}: learningFunction must be one of {sorted(ALLOWED_FUNCTIONS)}")

        layout = str(slide.get("layout") or "").strip()
        if layout not in ALLOWED_LAYOUTS:
            fails.append(f"{sid}: layout must be one of {sorted(ALLOWED_LAYOUTS)}")
        else:
            consecutive_layouts.append((sid, layout))

        asset_type = str(slide.get("assetType") or "").strip()
        if not asset_type:
            fails.append(f"{sid}: assetType is required when decision=use")

        bbox = slide.get("bbox")
        text_zone = slide.get("textSafeZone")
        if not _box_ok(bbox):
            fails.append(f"{sid}: bbox must be normalized x/y/w/h within 0..1")
        if not _box_ok(text_zone):
            fails.append(f"{sid}: textSafeZone must be normalized x/y/w/h within 0..1")

        if _box_ok(bbox) and _box_ok(text_zone):
            overlap = _intersection(bbox, text_zone)
            if overlap > 0.0025:
                fails.append(
                    f"{sid}: bbox overlaps textSafeZone by {overlap:.3f} normalized area; reserve separate seats before layout"
                )
            elif overlap > 0:
                warns.append(f"{sid}: bbox barely touches textSafeZone; add more safety margin")

            area = _area(bbox)
            if role not in {"icon-support", "mascot-cue"}:
                hero_count += 1
            if slide_type != "cover" and area > 0.55:
                warns.append(f"{sid}: visual occupies {area:.0%} of slide area; verify English/text remains dominant")
            if layout == "margin-mascot" and area > 0.25:
                warns.append(f"{sid}: margin mascot occupies {area:.0%}; target is about 25% or less")
            if layout == "micro-icon-support" and area > 0.12:
                warns.append(f"{sid}: micro-icon-support is too large ({area:.0%} of slide)")

        style = str(slide.get("styleFamily") or "").strip()
        if not style:
            fails.append(f"{sid}: styleFamily is required")
        else:
            style_counts[style] = style_counts.get(style, 0) + 1
            if default_style and style != default_style and not str(slide.get("styleExceptionReason") or "").strip():
                fails.append(
                    f"{sid}: styleFamily {style!r} differs from meta.defaultStyleFamily {default_style!r} without styleExceptionReason"
                )

        alt = str(slide.get("altText") or "").strip()
        if len(alt) < 8:
            fails.append(f"{sid}: altText must briefly describe the educational visual")

        embedded = slide.get("embeddedText", False)
        if embedded is True and not str(slide.get("textExceptionReason") or "").strip():
            fails.append(f"{sid}: embeddedText=true requires textExceptionReason; essential text should stay native/editable")

        source = slide.get("source")
        if not isinstance(source, dict):
            fails.append(f"{sid}: source object is required")
        else:
            kind = str(source.get("kind") or "").strip()
            if kind not in ALLOWED_SOURCE_KINDS:
                fails.append(f"{sid}: source.kind must be one of {sorted(ALLOWED_SOURCE_KINDS)}")
            if not str(source.get("provider") or "").strip():
                fails.append(f"{sid}: source.provider is required")
            if kind == "external":
                if not str(source.get("url") or "").strip():
                    fails.append(f"{sid}: external source requires source.url")
                if not str(source.get("license") or source.get("rights") or "").strip():
                    fails.append(f"{sid}: external source requires known license/usage rights")
            elif kind in {"generated", "local-owned"}:
                if not str(source.get("rights") or "").strip():
                    warns.append(f"{sid}: record source.rights for provenance")

        if asset_type.startswith("generated"):
            prompt = str(slide.get("prompt") or "").strip()
            if len(prompt) < 30:
                fails.append(f"{sid}: generated asset requires a production-ready prompt")
            if prompt and "no text" not in prompt.lower() and embedded is not True:
                warns.append(f"{sid}: generated prompt does not explicitly discourage text inside the image")

        recurring = slide.get("recurringCharacter")
        if isinstance(recurring, dict) and recurring.get("enabled") is True:
            reference = str(recurring.get("reference") or "").strip()
            if not reference:
                fails.append(f"{sid}: recurringCharacter.enabled=true requires a fixed reference/model sheet")

        if _has_placeholder(slide):
            fails.append(f"{sid}: unresolved placeholder token found")

    if used_count >= 6 and slides:
        usage_ratio = used_count / len(slides)
        if usage_ratio > 0.75:
            warns.append(
                f"deck: visuals are used on {usage_ratio:.0%} of slides; verify this is not decorative visual wallpaper"
            )

    # Repeating the same hero layout can make a deck look mechanically templated.
    if consecutive_layouts:
        run_layout = consecutive_layouts[0][1]
        run_ids = [consecutive_layouts[0][0]]
        for sid, layout in consecutive_layouts[1:]:
            if layout == run_layout:
                run_ids.append(sid)
                if len(run_ids) == 3:
                    warns.append(
                        f"deck: layout {run_layout!r} repeats on 3 consecutive visual slides ({', '.join(run_ids)}); check monotony"
                    )
            else:
                run_layout = layout
                run_ids = [sid]

    if len(style_counts) > 1:
        warns.append(f"deck: multiple style families present: {style_counts}; verify exceptions are intentional")

    return {
        "fail_count": len(fails),
        "warn_count": len(warns),
        "fails": fails,
        "warnings": warns,
        "summary": {
            "slides": len(slides),
            "visual_slides": used_count,
            "content_like_slides": content_like_count,
            "hero_visuals": hero_count,
            "style_families": style_counts,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Illustration Mode plan JSON")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()

    if not args.plan.exists():
        print(f"FAIL: file not found: {args.plan}")
        return 2

    try:
        data = json.loads(args.plan.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - CLI needs a readable message
        print(f"FAIL: invalid JSON: {exc}")
        return 2

    result = validate_plan(data)
    result["file"] = str(args.plan)

    if args.json_path:
        args.json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    for item in result["fails"]:
        print(f"FAIL: {item}")
    for item in result["warnings"]:
        print(f"WARN: {item}")

    print(
        f"Illustration plan QA: FAIL={result['fail_count']} WARN={result['warn_count']} "
        f"visual_slides={result['summary']['visual_slides']}/{result['summary']['slides']}"
    )
    return 1 if result["fail_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
