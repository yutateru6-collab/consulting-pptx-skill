#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
from lxml import etree

from check_click_reveal_xml import inspect

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

def P(tag): return f"{{{P_NS}}}{tag}"

def make_slide(path: Path, clicks: int = 6, break_fade: bool = False):
    sld = etree.Element(P("sld"), nsmap={"p": P_NS, "a": A_NS, "r": R_NS})
    csld = etree.SubElement(sld, P("cSld"))
    spTree = etree.SubElement(csld, P("spTree"))
    for sid in range(2, 2 + clicks + 1):
        pic = etree.SubElement(spTree, P("pic"))
        nv = etree.SubElement(pic, P("nvPicPr"))
        name = "BASE" if sid == 2 else f"CLICK{sid-2:02d}_part"
        etree.SubElement(nv, P("cNvPr"), id=str(sid), name=name)

    timing = etree.SubElement(sld, P("timing"))
    tnLst = etree.SubElement(timing, P("tnLst"))
    par0 = etree.SubElement(tnLst, P("par"))
    root = etree.SubElement(par0, P("cTn"), id="1", dur="indefinite", restart="never", nodeType="tmRoot")
    root_child = etree.SubElement(root, P("childTnLst"))
    seq = etree.SubElement(root_child, P("seq"))
    main = etree.SubElement(seq, P("cTn"), id="2", dur="indefinite", nodeType="mainSeq")
    main_child = etree.SubElement(main, P("childTnLst"))
    tid = 3
    for i in range(clicks):
        sid = str(i + 3)
        par = etree.SubElement(main_child, P("par"))
        click = etree.SubElement(par, P("cTn"), id=str(tid), nodeType="clickEffect", fill="hold", presetClass="entr", presetID="10"); tid += 1
        st = etree.SubElement(click, P("stCondLst")); etree.SubElement(st, P("cond"), delay="indefinite")
        child = etree.SubElement(click, P("childTnLst"))
        ip = etree.SubElement(child, P("par"))
        inner = etree.SubElement(ip, P("cTn"), id=str(tid), fill="hold"); tid += 1
        ist = etree.SubElement(inner, P("stCondLst")); etree.SubElement(ist, P("cond"), delay="0")
        ich = etree.SubElement(inner, P("childTnLst"))
        se = etree.SubElement(ich, P("set")); bh = etree.SubElement(se, P("cBhvr"))
        ct = etree.SubElement(bh, P("cTn"), id=str(tid), dur="1", fill="hold"); tid += 1
        cst = etree.SubElement(ct, P("stCondLst")); etree.SubElement(cst, P("cond"), delay="0")
        tgt = etree.SubElement(bh, P("tgtEl")); etree.SubElement(tgt, P("spTgt"), spid=sid)
        attrs = etree.SubElement(bh, P("attrNameLst")); etree.SubElement(attrs, P("attrName")).text = "style.visibility"
        to = etree.SubElement(se, P("to")); etree.SubElement(to, P("strVal"), val="visible")
        ae = etree.SubElement(ich, P("animEffect"), filter=("wipe" if break_fade and i == 0 else "fade"), transition="in")
        abh = etree.SubElement(ae, P("cBhvr"), additive="repl")
        act = etree.SubElement(abh, P("cTn"), id=str(tid), dur="350", fill="hold"); tid += 1
        ast = etree.SubElement(act, P("stCondLst")); etree.SubElement(ast, P("cond"), delay="0")
        at = etree.SubElement(abh, P("tgtEl")); etree.SubElement(at, P("spTgt"), spid=sid)
    prev = etree.SubElement(seq, P("prevCondLst")); pc = etree.SubElement(prev, P("cond"), evt="onPrev"); pt = etree.SubElement(pc, P("tgtEl")); etree.SubElement(pt, P("sldTgt"))
    nxt = etree.SubElement(seq, P("nextCondLst")); nc = etree.SubElement(nxt, P("cond"), evt="onNext"); nt = etree.SubElement(nc, P("tgtEl")); etree.SubElement(nt, P("sldTgt"))
    path.write_bytes(etree.tostring(sld, xml_declaration=True, encoding="UTF-8", standalone=True))


def main():
    with TemporaryDirectory() as td:
        td = Path(td)
        good = td / "good.xml"
        bad = td / "bad.xml"
        make_slide(good, clicks=6)
        make_slide(bad, clicks=6, break_fade=True)
        manifest = {"expected_clicks": 6, "click_order": [f"CLICK{i:02d}_part" for i in range(1, 7)]}
        good_result = inspect(good, manifest)
        bad_result = inspect(bad, manifest)
        assert good_result["fail_count"] == 0, good_result
        assert good_result["click_effects"] == 6, good_result
        assert bad_result["fail_count"] > 0, bad_result
        assert any("Fade entrance" in x for x in bad_result["fails"]), bad_result
    print("click-reveal XML regression tests: PASS")

if __name__ == "__main__":
    main()
