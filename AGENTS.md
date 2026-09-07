# Repository instructions for agents

This fork adds a **strict classroom-production layer** on top of the upstream consulting PPTX skill.

When the requested output is a **lesson, classroom, school, student-facing, English-teaching, grammar, vocabulary, reading, quiz, exam-review, or teaching PowerPoint**, Classroom Mode is mandatory.

## Files to read before producing a classroom deck

Read in this order:

1. `CLASSROOM.md`
2. `references/classroom-hard-gates-v3.md`
3. `references/classroom-slide-rules.md`
4. `references/classroom-delivery-contract.md`
5. `references/classroom-visual-qa-v3.md`
6. `references/slide-rules.md`

If the user says **flowchart / フローチャート / decision tree / 判断フロー**, also read:

- `references/classroom-flowchart-rules.md`

Classroom rules override generic consulting-layout preferences whenever they conflict.

## Non-negotiable completion rule

**Never call a classroom deck complete only because the PPTX opens or because the XML is valid.**

A classroom PPTX may be delivered as a finished file only after all of the following are true:

1. Source material has been checked for content fidelity.
2. `scripts/check_deck.py` exits 0.
3. `scripts/check_classroom_hard_gates.py` exits 0 in the correct profile.
4. `scripts/check_classroom_deck.py` exits 0.
5. Every slide has been rendered to PNG.
6. Every PNG has been visually inspected at near-full size, not only as a contact sheet.
7. The visual review has no unresolved high- or medium-severity issue.
8. After any fix, the entire deck has been rendered again.
9. `scripts/check_classroom_delivery.py` passes using the final machine-QA JSON and final visual-QA JSON.

If any of these steps cannot be executed, **do not describe the file as “完成版”, “確認済み”, “PASS”, or equivalent**. State that it is unverified and continue fixing with the tools that are available.

## Default classroom contract

Unless the user explicitly says otherwise:

- Every content slide must include substantive speaker notes.
- Classroom slides are click-driven: content is revealed in teaching order.
- Exercise/quiz slides must not show the answer at initial display.
- Cover title is at least 54pt; normal titles are at least 38pt.
- Normal body text is at least 24pt; short labels are at least 22pt.
- Important English text is at least 28pt and visually dominant.
- Body text is never shrunk to rescue a crowded layout.
- Rendered appearance is authoritative over PPTX coordinates.

Use `--allow-static` only when the user explicitly asks for no click animation.
Use `--notes-optional` only when the user explicitly says speaker notes are unnecessary.

## Flowchart requests

For any flowchart/decision-tree request, use `--profile flowchart` or allow `--profile auto` to infer it from the filename/cover. A flowchart request is not satisfied by a row or grid of rounded cards connected by decorative lines. The deck must have a persistent decision spine, explicit branch conditions, directional arrows, and branch zooms.

## GitHub Actions reporting rule

A green workflow is **not** evidence that a deck passed if the actual deck-QA step was skipped because no PPTX was present.

Never say “GitHub Actions checked the deck” unless the workflow logs show that the specific PPTX went through:

- general machine QA,
- classroom hard-gate QA,
- classroom layout QA,
- rendering,
- artifact generation.

If Actions cannot access a local/user-uploaded PPTX, run the same scripts locally and clearly say that this was the local equivalent, not Actions.
