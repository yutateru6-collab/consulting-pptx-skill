#!/usr/bin/env python3
"""Regression for absolute and relative OOXML speaker-note relationships."""
from __future__ import annotations

from io import BytesIO
from zipfile import ZipFile

from check_classroom_hard_gates import notes_text


def check_target(target: str) -> None:
    rels = (
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" '
        f'Target="{target}" Id="rId2"/></Relationships>'
    )
    notes = (
        '<p:notes xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r>'
        '<a:t>授業中の説明とクリック順を記す</a:t>'
        '</a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:notes>'
    )
    buf = BytesIO()
    with ZipFile(buf, "w") as zf:
        zf.writestr("ppt/slides/_rels/slide2.xml.rels", rels)
        zf.writestr("ppt/notesSlides/notesSlide2.xml", notes)
    buf.seek(0)
    with ZipFile(buf) as zf:
        assert notes_text(zf, 2) == "授業中の説明とクリック順を記す"


if __name__ == "__main__":
    check_target("/ppt/notesSlides/notesSlide2.xml")
    check_target("../notesSlides/notesSlide2.xml")
    print("CLASSROOM_NOTES_RELATIONSHIPS: PASS")
