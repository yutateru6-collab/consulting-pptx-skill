#!/usr/bin/env python3
"""Upload a PPTX to Google Drive and convert it to an editable Google Slides file.

Authentication uses Google Application Default Credentials (ADC).
The script verifies the created presentation by reading it back with Slides API.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
SLIDES_MIME = "application/vnd.google-apps.presentation"
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/presentations.readonly",
]


def _load_google() -> tuple[Any, Any, Any]:
    try:
        import google.auth
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError as exc:
        raise RuntimeError(
            "Google client libraries are missing. Run: pip install -r requirements-google-slides.txt"
        ) from exc
    return google.auth, build, MediaFileUpload


def upload(
    pptx: Path,
    title: str,
    parent_id: Optional[str] = None,
    expected_slides: Optional[int] = None,
) -> Dict[str, Any]:
    google_auth, build, MediaFileUpload = _load_google()
    credentials, project_id = google_auth.default(scopes=SCOPES)

    drive = build("drive", "v3", credentials=credentials, cache_discovery=False)
    body: Dict[str, Any] = {"name": title, "mimeType": SLIDES_MIME}
    if parent_id:
        body["parents"] = [parent_id]

    media = MediaFileUpload(str(pptx), mimetype=PPTX_MIME, resumable=True)
    created = (
        drive.files()
        .create(
            body=body,
            media_body=media,
            fields="id,name,mimeType,webViewLink,parents",
            supportsAllDrives=True,
        )
        .execute()
    )

    presentation_id = created["id"]
    slides = build("slides", "v1", credentials=credentials, cache_discovery=False)
    presentation = slides.presentations().get(presentationId=presentation_id).execute()
    page_count = len(presentation.get("slides", []))

    result: Dict[str, Any] = {
        "status": "PASS",
        "presentationId": presentation_id,
        "name": created.get("name"),
        "mimeType": created.get("mimeType"),
        "webViewLink": created.get("webViewLink"),
        "parents": created.get("parents", []),
        "slideCount": page_count,
        "expectedSlides": expected_slides,
        "projectId": project_id,
        "verification": "Slides API read-back completed; visual fidelity is not verified by this script.",
    }

    if created.get("mimeType") != SLIDES_MIME:
        result["status"] = "FAIL"
        result["error"] = "Drive did not create a Google Slides MIME type."
    if expected_slides is not None and page_count != expected_slides:
        result["status"] = "FAIL"
        result["error"] = f"Slide count mismatch: expected {expected_slides}, got {page_count}."
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--title", help="Google Slides file name; defaults to PPTX stem.")
    parser.add_argument("--parent-id", help="Optional Google Drive folder ID.")
    parser.add_argument("--expected-slides", type=int, help="Fail if converted slide count differs.")
    parser.add_argument("--json", dest="json_out", type=Path, help="Write result JSON.")
    args = parser.parse_args()

    if not args.pptx.is_file():
        print(f"FAIL: PPTX not found: {args.pptx}", file=sys.stderr)
        return 2
    if args.pptx.suffix.lower() != ".pptx":
        print("FAIL: input must be a .pptx file", file=sys.stderr)
        return 2

    try:
        result = upload(
            pptx=args.pptx,
            title=args.title or args.pptx.stem,
            parent_id=args.parent_id,
            expected_slides=args.expected_slides,
        )
    except Exception as exc:
        result = {"status": "FAIL", "error": str(exc)}

    text = json.dumps(result, ensure_ascii=False, indent=2)
    print(text)
    if args.json_out:
        args.json_out.write_text(text + "\n", encoding="utf-8")
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
