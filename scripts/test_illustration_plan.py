#!/usr/bin/env python3
from copy import deepcopy

from check_illustration_plan import validate_plan


def good_plan():
    return {
        "meta": {
            "deckId": "demo",
            "defaultStyleFamily": "clean-flat-education",
            "outputTarget": "pptx",
        },
        "slides": [
            {
                "slideId": "s01",
                "slideType": "content",
                "decision": "use",
                "reason": "文法の意味を具体場面で理解させるため",
                "role": "scene",
                "learningFunction": "concretize",
                "assetType": "generated-illustration",
                "layout": "text-left-visual-right",
                "bbox": {"x": 0.65, "y": 0.2, "w": 0.28, "h": 0.5},
                "textSafeZone": {"x": 0.05, "y": 0.18, "w": 0.52, "h": 0.58},
                "styleFamily": "clean-flat-education",
                "embeddedText": False,
                "prompt": "A clean educational scene showing a student finishing a book, no text, simple light background.",
                "altText": "本を読み終えた直後の生徒の場面",
                "source": {
                    "kind": "generated",
                    "provider": "image-generation-tool",
                    "rights": "generated for this deck",
                },
                "recurringCharacter": {"enabled": False, "reference": None},
            },
            {
                "slideId": "s02",
                "slideType": "content",
                "decision": "omit",
                "reason": "英文の形そのものを比較するページで絵が不要なため",
            },
        ],
    }


def main():
    ok = validate_plan(good_plan())
    assert ok["fail_count"] == 0, ok

    overlap = deepcopy(good_plan())
    overlap["slides"][0]["bbox"] = {"x": 0.50, "y": 0.2, "w": 0.35, "h": 0.5}
    bad = validate_plan(overlap)
    assert bad["fail_count"] > 0, bad
    assert any("overlaps textSafeZone" in x for x in bad["fails"]), bad

    style_drift = deepcopy(good_plan())
    style_drift["slides"][0]["styleFamily"] = "manga"
    bad = validate_plan(style_drift)
    assert any("styleFamily" in x for x in bad["fails"]), bad

    recurring = deepcopy(good_plan())
    recurring["slides"][0]["recurringCharacter"] = {"enabled": True, "reference": ""}
    bad = validate_plan(recurring)
    assert any("model sheet" in x for x in bad["fails"]), bad

    external = deepcopy(good_plan())
    external["slides"][0]["assetType"] = "external-svg"
    external["slides"][0]["source"] = {"kind": "external", "provider": "example"}
    bad = validate_plan(external)
    assert any("source.url" in x for x in bad["fails"]), bad
    assert any("license" in x for x in bad["fails"]), bad

    print("illustration plan regression tests: PASS")


if __name__ == "__main__":
    main()
