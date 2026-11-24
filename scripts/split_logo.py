"""Separa el logo vectorial en montaña y texto (sin la franja inferior).

Reconstruye cada trazo del PDF como <path> SVG a partir de sus comandos
(líneas y curvas), así que la salida sigue siendo vectorial.
"""
import sys
import pymupdf

PDF = r"C:/Users/nache/Desktop/LOGO_VECTOR_SHARPA_ANTONIO_SALGUERO.pdf"
OUT = r"C:/Users/nache/Documents/Sherpa/assets"

doc = pymupdf.open(PDF)
page = doc[0]
drawings = page.get_drawings()


def fmt(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


def drawing_path(dr):
    parts = []
    cur = None
    for it in dr["items"]:
        kind = it[0]
        if kind == "l":
            p1, p2 = it[1], it[2]
            if cur is None or (abs(cur.x - p1.x) > 1e-3 or abs(cur.y - p1.y) > 1e-3):
                parts.append(f"M{fmt(p1.x)} {fmt(p1.y)}")
            parts.append(f"L{fmt(p2.x)} {fmt(p2.y)}")
            cur = p2
        elif kind == "c":
            p1, p2, p3, p4 = it[1], it[2], it[3], it[4]
            if cur is None or (abs(cur.x - p1.x) > 1e-3 or abs(cur.y - p1.y) > 1e-3):
                parts.append(f"M{fmt(p1.x)} {fmt(p1.y)}")
            parts.append(
                f"C{fmt(p2.x)} {fmt(p2.y)} {fmt(p3.x)} {fmt(p3.y)} {fmt(p4.x)} {fmt(p4.y)}"
            )
            cur = p4
        elif kind == "re":
            r = it[1]
            parts.append(
                f"M{fmt(r.x0)} {fmt(r.y0)}H{fmt(r.x1)}V{fmt(r.y1)}H{fmt(r.x0)}Z"
            )
            cur = None
        elif kind == "qu":
            q = it[1]
            parts.append(
                f"M{fmt(q.ul.x)} {fmt(q.ul.y)}L{fmt(q.ur.x)} {fmt(q.ur.y)}"
                f"L{fmt(q.lr.x)} {fmt(q.lr.y)}L{fmt(q.ll.x)} {fmt(q.ll.y)}Z"
            )
            cur = None
    return "".join(parts)


def rgb_hex(c):
    if c is None:
        return None
    r, g, b = (round(x * 255) for x in c[:3])
    return f"#{r:02x}{g:02x}{b:02x}"


def build_svg(selected, name):
    if not selected:
        sys.exit(f"ABORT: no drawings selected for {name}")
    bb = pymupdf.Rect()
    for dr in selected:
        bb |= dr["rect"]
    pad = 1.0
    x0, y0 = bb.x0 - pad, bb.y0 - pad
    w, h = bb.width + 2 * pad, bb.height + 2 * pad
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fmt(x0)} {fmt(y0)} {fmt(w)} {fmt(h)}"'
        f' width="{fmt(w)}" height="{fmt(h)}">'
    ]
    for dr in selected:
        d = drawing_path(dr)
        if not d:
            continue
        fill = rgb_hex(dr.get("fill"))
        rule = ' fill-rule="evenodd"' if dr.get("even_odd") else ""
        attrs = f' fill="{fill}"' if fill else ' fill="none"'
        stroke = rgb_hex(dr.get("color"))
        if stroke and not fill:
            attrs = f' fill="none" stroke="{stroke}" stroke-width="{fmt(dr.get("width") or 1)}"'
        out.append(f'<path d="{d}"{attrs}{rule}/>')
    out.append("</svg>")
    path = f"{OUT}/{name}.svg"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print(name, "paths:", len(selected), "viewBox:", fmt(x0), fmt(y0), fmt(w), fmt(h))


mountain = [d for d in drawings if d["rect"].y1 <= 310 and d["rect"].y0 < 260]
letters = [d for d in drawings if d["rect"].y0 >= 286 and d["rect"].y0 < 420 and d["rect"].y1 <= 430]
tagline = [d for d in drawings if d["rect"].y0 >= 420 and d["rect"].y1 <= 480]

used = {id(d) for d in mountain + letters + tagline}
dropped = [d for d in drawings if id(d) not in used]
print("dropped (franja inferior):", len(dropped), "rects:", [tuple(round(v) for v in d["rect"]) for d in dropped])

build_svg(mountain, "sherpa-mountain")
build_svg(letters + tagline, "sherpa-wordmark")
