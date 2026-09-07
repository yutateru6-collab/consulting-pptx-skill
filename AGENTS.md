# Repository instructions for agents

This fork adds a classroom-specific layer on top of the upstream consulting PPTX skill.

When the requested output is a **lesson, classroom, school, student-facing, English-teaching, grammar, vocabulary, reading, quiz, or exam-review PowerPoint**, read these files before producing the deck:

1. `CLASSROOM.md`
2. `references/classroom-slide-rules.md`
3. `references/classroom-visual-qa-prompt.md`
4. `references/slide-rules.md`

For classroom decks, the classroom rules override generic consulting-layout preferences when they conflict.

Never declare a classroom deck complete from PPTX structure alone. Run both machine checkers, render every slide to PNG, inspect the PNGs, fix defects, and render again.
