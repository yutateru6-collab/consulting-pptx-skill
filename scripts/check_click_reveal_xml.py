#!/usr/bin/env python3
"""Validate PowerPoint on-click entrance animation structure in a slide XML.

This checker is intentionally XML-level. It verifies the same timing structure
PowerPoint writes for a click-triggered Fade entrance: clickEffect -> set
style.visibility=visible -> animEffect(filter=fade, transition=in), with valid
shape targets and presenter-controlled next/previous conditions.

It does NOT claim to be a Microsoft PowerPoint runtime playback test.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from lxml import etree

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS = {"p": P_NS}
CLICK_NAME_RE = re.compile(r"^CLICK(\d{2})_")


def _uniq(seq):
    out = []
    for x in seq:
        if x not in out:
            out.append(x)
    return out


def inspect(slide_xml: Path, manifest: dict | None = None) -> dict:
    root = etree.parse(str(slide_xml)).getroot()
    fails: list[str] = []
    warns: list[str] = []

    shapes = {
        el.get("id"): el.get("name", "")
        for el in root.findall(".//p:cNvPr", NS)
        if el.get("id")
    }

    timing = root.find("p:timing", NS)
    if timing is None:
        fails.append("slide has no p:timing element")
        return {
            "file": str(slide_xml), "fail_count": len(fails), "warn_count": 0,
            "fails": fails, "warnings": [], "clicks": []
        }

    transition = root.find("p:transition", NS)
    if transition is not None and transition.get("advTm") is not None:
        fails.append("automatic slide advance (advTm) is enabled")

    node_ids = [x.get("id") for x in timing.findall(".//p:cTn", NS) if x.get("id")]
    dup_ids = sorted({x for x in node_ids if node_ids.count(x) > 1})
    if dup_ids:
        fails.append(f"duplicate animation time-node IDs: {dup_ids[:10]}")

    click_nodes = timing.findall(".//p:cTn[@nodeType='clickEffect']", NS)
    click_results = []
    target_names = []

    for index, click in enumerate(click_nodes, start=1):
        targets = _uniq([
            x.get("spid") for x in click.findall(".//p:spTgt", NS) if x.get("spid")
        ])
        if len(targets) != 1:
            fails.append(f"click {index}: expected exactly one unique target, got {targets}")
            target_id = targets[0] if targets else None
        else:
            target_id = targets[0]

        target_name = shapes.get(target_id, "") if target_id else ""
        if target_id and target_id not in shapes:
            fails.append(f"click {index}: target shape id {target_id} does not exist")
        if target_id and not CLICK_NAME_RE.match(target_name):
            fails.append(
                f"click {index}: target {target_id} name {target_name!r} does not use CLICKnn_ prefix"
            )

        st_delays = [x.get("delay") for x in click.findall("p:stCondLst/p:cond", NS)]
        if "indefinite" not in st_delays:
            fails.append(f"click {index}: clickEffect is not waiting for an indefinite/user click trigger")

        set_nodes = click.findall(".//p:set", NS)
        good_visibility = False
        for set_node in set_nodes:
            set_targets = {x.get("spid") for x in set_node.findall(".//p:spTgt", NS)}
            attrs = [x.text for x in set_node.findall(".//p:attrName", NS)]
            vals = [x.get("val") for x in set_node.findall(".//p:to/p:strVal", NS)]
            if target_id in set_targets and "style.visibility" in attrs and "visible" in vals:
                good_visibility = True
        if not good_visibility:
            fails.append(f"click {index}: missing visibility=visible set action for target {target_id}")

        fades = click.findall(".//p:animEffect", NS)
        good_fade = False
        for fade in fades:
            fade_targets = {x.get("spid") for x in fade.findall(".//p:spTgt", NS)}
            if (
                target_id in fade_targets
                and fade.get("filter") == "fade"
                and fade.get("transition") == "in"
            ):
                good_fade = True
        if not good_fade:
            fails.append(f"click {index}: missing Fade entrance effect for target {target_id}")

        if target_name:
            target_names.append(target_name)
        click_results.append({
            "index": index,
            "target_id": target_id,
            "target_name": target_name,
            "visibility_set": good_visibility,
            "fade_in": good_fade,
        })

    next_events = [x.get("evt") for x in timing.findall(".//p:nextCondLst/p:cond", NS)]
    prev_events = [x.get("evt") for x in timing.findall(".//p:prevCondLst/p:cond", NS)]
    if "onNext" not in next_events:
        fails.append("main animation sequence is missing onNext slide target condition")
    if "onPrev" not in prev_events:
        warns.append("main animation sequence is missing onPrev slide target condition")

    if manifest:
        expected_clicks = manifest.get("expected_clicks")
        if expected_clicks is not None and len(click_nodes) != expected_clicks:
            fails.append(f"expected {expected_clicks} clickEffect nodes, found {len(click_nodes)}")
        expected_order = manifest.get("click_order") or []
        if expected_order and target_names != expected_order:
            fails.append(f"click order mismatch: expected {expected_order}, got {target_names}")

    return {
        "file": str(slide_xml),
        "fail_count": len(fails),
        "warn_count": len(warns),
        "fails": fails,
        "warnings": warns,
        "shape_count": len(shapes),
        "click_effects": len(click_nodes),
        "clicks": click_results,
        "next_condition": "onNext" in next_events,
        "prev_condition": "onPrev" in prev_events,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slide_xml", type=Path)
    ap.add_argument("--manifest", type=Path)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    if not args.slide_xml.exists():
        print(f"FAIL: missing slide XML: {args.slide_xml}", file=sys.stderr)
        return 2

    manifest = None
    if args.manifest:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))

    result = inspect(args.slide_xml, manifest)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    for item in result["fails"]:
        print("FAIL:", item)
    for item in result["warnings"]:
        print("WARN:", item)
    print(
        f"click-reveal QA: clicks={result['click_effects']} "
        f"fail={result['fail_count']} warn={result['warn_count']}"
    )
    return 1 if result["fail_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
