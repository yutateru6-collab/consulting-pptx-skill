---
name: classroom-illustration
description: Use when adding illustrations, generated images, SVGs, icons, mascot art, or other supporting visuals to classroom or education slides. Plans whether a visual is needed, reserves its layout zone before text placement, keeps style consistent, records provenance, and checks image/text collisions in editable PPTX decks.
---

# Classroom Illustration Skill

Use this skill when a classroom/education deck needs illustrations or other visual assets. The goal is not to maximize image count; it is to add only the visuals that make a concept easier to understand, remember, compare, or apply.

## Read first

1. `../../ILLUSTRATION.md`
2. `../../references/illustration-mode.md`
3. `../../references/classroom-layout-safety.md`
4. For English lessons, also follow `../../EDUCATION.md`

## Workflow

### 1. Decide whether each slide needs a visual

For every slide, choose `use` or `omit` before generating or searching for artwork.

Use a visual when it provides a cognitive anchor such as:

- a concrete scene for an abstract grammar meaning
- a before/after or A/B contrast
- a temporal/state change
- a process or route
- a memorable concept metaphor
- a recurring mascot that performs a meaningful action

Omit the visual when it is only filling whitespace, repeating text, or competing with the main English sentence.

### 2. Write an Illustration Plan

Start from `../../templates/illustration-plan.example.json` and validate it:

```bash
python3 ../../scripts/check_illustration_plan.py illustration-plan.json --json illustration-plan-qa.json
```

Do not move to production with any FAIL.

### 3. Reserve layout space before adding text

Choose one layout before rendering the slide:

- `text-left-visual-right`
- `visual-left-text-right`
- `paired-scenes`
- `scene-plus-takeaway`
- `margin-mascot`
- `micro-icon-support`

Define an explicit visual `bbox` and a non-overlapping `textSafeZone`. Never finish the text layout and then squeeze the image into leftover space.

### 4. Acquire or generate the asset

Preferred order depends on the task:

- Generate a custom illustration when a precise educational scene or recurring character is needed.
- Use a clean vector/SVG or icon when the concept is generic and a custom scene adds little value.
- Use an external image only when its source and usage rights are known.

For generated illustrations:

- one core idea per image
- no essential instructional text baked into the image
- ask for a simple background or transparency appropriate to the reserved zone
- match the deck's fixed `styleFamily`
- for recurring characters, use the same reference/model sheet every time

### 5. Place the asset safely

- Preserve aspect ratio; fit or intentionally crop, never stretch.
- Keep captions and essential labels as native slide text.
- Keep normal images out of the text-safe zone.
- Background/full-bleed art requires deliberate naming and separate contrast review.
- Do not use a large hero visual on an already dense 3-column teaching slide.

### 6. Run PPTX visual-asset QA

```bash
python3 ../../scripts/check_classroom_visual_assets.py deck.pptx --json visual-assets-qa.json
```

Fix all FAILs. Then render the final PPTX to PNG and inspect every slide at near-full size.

## English-teaching defaults

- Tense/aspect: use scenes and state contrast, not decorative mascots.
- Present perfect: visualize the present result/connection, not only the past action.
- Count/noncount: show countable units vs amount/substance.
- Prepositions: use one clean spatial scene.
- Conditionals/subjunctive: show reality vs imagined alternative.
- Vocabulary: prefer a usage scene over a standalone clip-art object.
- Reading: illustrate only structural turns or major concepts, not every paragraph.

## Reject these patterns

- illustration in the bottom-right corner with no teaching role
- a different art style on every slide
- generated art covering English examples or answer choices
- important wording embedded inside a raster image
- forcing three hero visuals into a three-column explanation
- shrinking classroom text to make room for art
- using an external asset when the license/source is unknown

## Source acknowledgements

The design approach is informed by public presentation/illustration skills including `wshobson/agents` (`pptx-visual-assets`), `lgwanai/ppt-skill`, and `AppajiDheeraj/paper-engine-illustrations`. This skill is independently written for this repository and does not assume that third-party assets are bundled or licensed for redistribution here.
