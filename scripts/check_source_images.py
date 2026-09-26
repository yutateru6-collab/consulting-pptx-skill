#!/usr/bin/env python3
"""Verify regenerated explanatory panels are embedded as dominant PPTX pictures.

Usage: python3 scripts/check_source_images.py deck.pptx image-manifest.json
Pillow is required to compare crop pixels with the declared source region.
"""

import hashlib
import json
import posixpath
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    from PIL import Image, ImageChops
except ImportError:
    sys.exit("FAIL: Pillow が必要です（python3 -m pip install Pillow）")

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
EMU_PER_INCH = 914400
DISPLAY_DPI = 96
MIN_PANEL_AREA = 0.30


def digest(data):
    return hashlib.sha256(data).hexdigest()


def local_path(manifest_path, value):
    if not isinstance(value, str) or not value:
        raise ValueError("manifest のファイルパスが空です")
    path = Path(value)
    return path if path.is_absolute() else manifest_path.parent / path


def slide_pictures(package, slide_number):
    slide_part = f"ppt/slides/slide{slide_number}.xml"
    rel_part = f"ppt/slides/_rels/slide{slide_number}.xml.rels"
    names = set(package.namelist())
    if slide_part not in names or rel_part not in names:
        raise ValueError(f"スライド {slide_number} または画像用の関連付けがありません")

    rel_root = ET.fromstring(package.read(rel_part))
    rels = {}
    for rel in rel_root.findall(f"{{{PR}}}Relationship"):
        if rel.get("TargetMode") == "External":
            continue
        target = rel.get("Target", "")
        if rel.get("Type", "").endswith("/image"):
            rels[rel.get("Id")] = (target.lstrip("/") if target.startswith("/") else
                                   posixpath.normpath(posixpath.join("ppt/slides", target)))

    root = ET.fromstring(package.read(slide_part))
    pictures = []
    for pic in root.iter(f"{{{P}}}pic"):
        blip = pic.find(f".//{{{A}}}blip")
        ext = pic.find(f".//{{{P}}}spPr/{{{A}}}xfrm/{{{A}}}ext")
        if blip is None or ext is None:
            continue
        media_part = rels.get(blip.get(f"{{{R}}}embed"))
        if media_part is None or media_part not in names:
            continue
        width_px = int(ext.get("cx", "0")) / EMU_PER_INCH * DISPLAY_DPI
        height_px = int(ext.get("cy", "0")) / EMU_PER_INCH * DISPLAY_DPI
        pictures.append((digest(package.read(media_part)), width_px, height_px))
    return pictures


def check(pptx_path, manifest_path):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assets = manifest.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValueError("manifest に1件以上の assets が必要です")

    source = local_path(manifest_path, manifest.get("source_image"))
    with Image.open(source) as source_image, zipfile.ZipFile(pptx_path) as package:
        slide_count = len([n for n in package.namelist()
                           if n.startswith("ppt/slides/slide") and n.endswith(".xml")])
        presentation = ET.fromstring(package.read("ppt/presentation.xml"))
        size = presentation.find(f"{{{P}}}sldSz")
        if size is None:
            raise ValueError("PPTXのスライド寸法を読み取れません")
        slide_area_px = (int(size.get("cx")) / EMU_PER_INCH * DISPLAY_DPI *
                         int(size.get("cy")) / EMU_PER_INCH * DISPLAY_DPI)
        content_slides = manifest.get("content_slides")
        if (not isinstance(content_slides, list) or not content_slides or
                any(type(n) is not int or n < 1 or n > slide_count for n in content_slides) or
                len(content_slides) != len(set(content_slides))):
            raise ValueError("content_slides に全内容スライドの有効で重複のない番号が必要です")
        panel_coverage = {n: 0.0 for n in content_slides}
        used = set()
        for item in assets:
            name = item.get("name")
            if not isinstance(name, str) or not name or name in used:
                raise ValueError(f"asset name が空か重複しています: {name!r}")
            used.add(name)
            role = item.get("role")
            if role not in {"explanation_panel", "title_panel", "illustration"}:
                raise ValueError(f"{name}: role は explanation_panel / title_panel / illustration のいずれかが必要です")
            box = item.get("source_crop_box")
            if not isinstance(box, list) or len(box) != 4 or not all(type(v) is int for v in box):
                raise ValueError(f"{name}: source_crop_box は4個の整数が必要です")
            left, top, right, bottom = box
            if not (0 <= left < right <= source_image.width and
                    0 <= top < bottom <= source_image.height):
                raise ValueError(f"{name}: 切り抜き範囲が元画像からはみ出しています")

            crop_path = local_path(manifest_path, item.get("source_crop_file"))
            generated_path = local_path(manifest_path, item.get("regenerated_png"))
            with Image.open(crop_path) as crop_image:
                if crop_image.size != (right-left, bottom-top):
                    raise ValueError(f"{name}: 切り抜きファイルの寸法が範囲と一致しません")
                diff = ImageChops.difference(source_image.crop(tuple(box)).convert("RGBA"),
                                             crop_image.convert("RGBA"))
                if diff.getbbox() is not None:
                    raise ValueError(f"{name}: 切り抜きファイルが元画像の指定画素と一致しません")
            with Image.open(generated_path) as generated:
                if generated.format != "PNG":
                    raise ValueError(f"{name}: 再生成ファイルはPNGが必要です")
                generated_size = generated.size
            generated_hash = digest(generated_path.read_bytes())
            if generated_hash == digest(crop_path.read_bytes()):
                raise ValueError(f"{name}: 切り抜きそのものを再生成PNGとして指定しています")

            slides = item.get("slides")
            if (not isinstance(slides, list) or not slides or
                    any(type(n) is not int or n < 1 or n > slide_count for n in slides) or
                    len(slides) != len(set(slides))):
                raise ValueError(f"{name}: slides に有効で重複のない番号が必要です")
            for number in slides:
                matches = [(w, h) for image_hash, w, h in slide_pictures(package, number)
                           if image_hash == generated_hash]
                if not matches:
                    raise ValueError(f"{name}: スライド {number} に再生成PNGの画像オブジェクトがありません")
                for display_w, display_h in matches:
                    if (generated_size[0] < 2*display_w or
                            generated_size[1] < 2*display_h):
                        raise ValueError(f"{name}: スライド {number} の表示枠に対して画素数が2倍未満です")
                    if role == "explanation_panel" and number in panel_coverage:
                        panel_coverage[number] = max(panel_coverage[number],
                                                     display_w * display_h / slide_area_px)
            print(f"PASS {name} ({role}): source crop {right-left}×{bottom-top} → PNG {generated_size[0]}×{generated_size[1]} → slides {slides}")
        for number, area in panel_coverage.items():
            if area < MIN_PANEL_AREA:
                raise ValueError(f"スライド {number}: 説明パネル画像がありません、または表示面積が{MIN_PANEL_AREA:.0%}未満です（{area:.1%}）")
            print(f"PASS slide {number}: explanation panel area {area:.1%}")
    print(f"PASS: {len(assets)} assets / {len(content_slides)} content slides; explanatory pictures verified. Text accuracy requires visual review")


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 scripts/check_source_images.py deck.pptx image-manifest.json")
    try:
        check(Path(sys.argv[1]), Path(sys.argv[2]).resolve())
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
        sys.exit(f"FAIL: {exc}")


if __name__ == "__main__":
    main()
