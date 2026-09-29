#!/usr/bin/env python3
"""Plan view of the carrier PCB (PCB1), in board-local mm.

Origin is the board's bottom-left corner. The board is an L: a full-length
lane carrying both pogo pins and the output path, plus a main body under the
IP2326 module and the TPS630702 regulator.

Usage:  python scripts/pcb_svg.py
Output: hardware/bom/PCB1-carrier/pcb-layout.svg
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "hardware" / "bom" / "PCB1-carrier"
SCALE, MARGIN = 9.0, 70.0

W, H = 80.0, 44.0          # board extent
LANE_H = 10.0              # lane height
BODY_X = 43.0              # main body starts here
HOLE_D = 2.2               # M2 clearance

# ref, label, w, h, (cx, cy), class
PARTS = [
    # --- lane ---
    ("P1a", "pogo", 2.1, 2.1, (18.0, 7.0), "pogo"),
    ("P1b", "pogo", 2.1, 2.1, (68.0, 7.0), "pogo"),
    ("J3", "balance XH-3", 11.0, 6.0, (10.5, 6.0), "conn"),
    ("SW1", "slide", 7.0, 4.0, (24.5, 2.2), "conn"),
    ("J2", "pack XH-2", 8.0, 5.0, (25.0, 7.3), "conn"),
    ("C1a", "220u", 8.0, 8.0, (33.0, 5.0), "pwr"),
    ("C1b", "220u", 8.0, 8.0, (42.0, 5.0), "pwr"),
    ("D1", "SS34", 5.0, 3.0, (49.0, 5.0), "pwr"),
    ("R1", "R1", 6.0, 3.0, (56.0, 5.0), "pwr"),
    ("F1", "PTC 1812", 4.5, 3.2, (61.5, 5.0), "pwr"),
    ("J4", "U2 link 5-way", 10.0, 3.0, (75.0, 6.0), "conn"),
    # --- main body ---
    ("U2", "IP2326 module", 31.0, 18.0, (64.5, 20.0), "mod"),
    ("U3", "TPS630702", 3.0, 2.5, (47.0, 36.0), "ic"),
    ("L1", "1.5uH", 4.0, 4.0, (52.0, 36.0), "pwr"),
    ("Cout", "3x22u", 6.5, 2.0, (58.0, 33.0), "pwr"),
    ("Cin", "2x10u", 4.5, 2.0, (49.0, 40.0), "pwr"),
    ("R2/R3", "FB 649k/100k", 4.0, 1.5, (48.0, 31.5), "sig"),
    ("Q1", "2N7002", 3.0, 3.0, (56.0, 40.0), "sig"),
    ("R4/R5", "interlock 100k", 4.0, 1.5, (62.0, 40.0), "sig"),
    ("R6/R7", "EN uvlo 698k/100k", 4.0, 1.5, (69.0, 40.0), "sig"),
]
PCB_HOLES = [(3.0, 3.0), (77.0, 3.0), (45.5, 41.5), (77.0, 41.5)]
MOD_HOLES = [(51.0, 13.0), (78.0, 13.0), (51.0, 27.0), (78.0, 27.0)]

def hit(a, b):
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah

def rect(p):
    _r, _l, w, h, (cx, cy), _c = p
    return (cx - w / 2, cy - h / 2, w, h)

def build():
    X = lambda v: MARGIN + v * SCALE
    Y = lambda v: MARGIN + (H - v) * SCALE          # y up
    WIDTH = W * SCALE + 2 * MARGIN
    HEIGHT = H * SCALE + 2 * MARGIN + 150
    p = []; a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH:.0f}" height="{HEIGHT:.0f}" '
      f'viewBox="0 0 {WIDTH:.0f} {HEIGHT:.0f}" font-family="ui-sans-serif,system-ui,sans-serif">')
    a('<style>'
      '.t{font-size:9px;fill:#111}.s{font-size:7px;fill:#555}.ttl{font-size:16px;font-weight:600;fill:#111}'
      '.pcb{fill:#1f6f43;fill-opacity:.10;stroke:#1f6f43;stroke-width:2}'
      '.mod{fill:#e7d9f5;stroke:#7a4fd0;stroke-width:1.2}'
      '.ic{fill:#ffd9d9;stroke:#c0392b;stroke-width:1.2}'
      '.pwr{fill:#ffeccc;stroke:#c98a1a;stroke-width:1}'
      '.conn{fill:#d6ecff;stroke:#2c7bb6;stroke-width:1}'
      '.sig{fill:#e4e4e4;stroke:#777;stroke-width:.8}'
      '.pogo{fill:#fff2b8;stroke:#b8860b;stroke-width:1.4}'
      '</style>')
    a(f'<rect width="{WIDTH:.0f}" height="{HEIGHT:.0f}" fill="#fff"/>')
    a(f'<text x="{MARGIN}" y="28" class="ttl">PCB1 carrier — plan view, component side</text>')
    a(f'<text x="{MARGIN}" y="46" class="s">{W:g} x {H:g} mm · L-shape · 1 mm = {SCALE:g} px · '
      f'origin bottom-left · pogo pins mount on the UNDERSIDE</text>')
    # outline
    pts = [(0,0),(W,0),(W,H),(BODY_X,H),(BODY_X,LANE_H),(0,LANE_H)]
    a('<polygon points="' + " ".join(f"{X(x):.1f},{Y(y):.1f}" for x,y in pts) + '" class="pcb"/>')
    a(f'<line x1="{X(0):.1f}" y1="{Y(LANE_H):.1f}" x2="{X(W):.1f}" y2="{Y(LANE_H):.1f}" '
      f'stroke="#1f6f43" stroke-width=".8" stroke-dasharray="5 3"/>')
    a(f'<text x="{X(1):.1f}" y="{Y(LANE_H)+13:.1f}" class="s" fill="#1f6f43">lane — pogo pins + output path, no tall parts</text>')
    # holes
    for (x,y) in PCB_HOLES:
        a(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{HOLE_D/2*SCALE:.1f}" fill="#fff" stroke="#333" stroke-width="1.2"/>')
    for (x,y) in MOD_HOLES:
        a(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{HOLE_D/2*SCALE:.1f}" fill="#fff" stroke="#7a4fd0" stroke-width="1" stroke-dasharray="2 2"/>')
    # parts
    for pt in PARTS:
        ref, lab, w, h, (cx, cy), cls = pt
        rx, ry = cx - w/2, cy - h/2
        if cls == "pogo":
            a(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{w/2*SCALE:.1f}" class="pogo"/>')
        else:
            a(f'<rect x="{X(rx):.1f}" y="{Y(ry+h):.1f}" width="{w*SCALE:.1f}" height="{h*SCALE:.1f}" class="{cls}" rx="2"/>')
        if w >= 7 and h >= 5:
            a(f'<text x="{X(cx):.1f}" y="{Y(cy)-1:.1f}" class="t" text-anchor="middle">{ref}</text>')
            a(f'<text x="{X(cx):.1f}" y="{Y(cy)+9:.1f}" class="s" text-anchor="middle">{lab}</text>')
        else:
            a(f'<text x="{X(cx):.1f}" y="{Y(cy+h/2)-4:.1f}" class="s" text-anchor="middle">{ref}</text>')
    # legend
    ly = MARGIN + H*SCALE + 34
    for i,(col,txt) in enumerate([("#e7d9f5","module (U2, on standoffs)"),("#ffd9d9","regulator IC"),
                                  ("#ffeccc","power path"),("#d6ecff","connector / switch"),
                                  ("#e4e4e4","signal"),("#fff2b8","pogo pin (underside)")]):
        cx = MARGIN + (i % 3) * 250; cy = ly + (i // 3) * 20
        a(f'<rect x="{cx}" y="{cy-9}" width="13" height="13" fill="{col}" stroke="#555" stroke-width=".8"/>')
        a(f'<text x="{cx+19}" y="{cy+1}" class="s">{txt}</text>')
    notes = [
        "J2 pack power (XH-2) from U1 protection board P+/P-   ·   J3 balance (XH-3), midpoint to U2 BM",
        "J4 links the IP2326 module: VIN+, GND, B+, B-, BM   ·   solid circles = M2 board holes, dashed = U2 module holes",
        "SW1 sits in series with the R6/R7 top leg, so switching off also removes the 9.3 uA divider draw",
        "Q1 pulls EN low whenever VBUS is present - cannot charge and shoot at once",
    ]
    for i,t in enumerate(notes):
        a(f'<text x="{MARGIN}" y="{ly+52+i*15:.0f}" class="s">{t}</text>')
    a('</svg>')
    return "\n".join(p)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / "pcb-layout.svg"
    f.write_text(build(), encoding="utf-8")
    bad = []
    for i in range(len(PARTS)):
        for j in range(i+1, len(PARTS)):
            if hit(rect(PARTS[i]), rect(PARTS[j])):
                bad.append((PARTS[i][0], PARTS[j][0]))
    for (x,y) in PCB_HOLES:
        hr = (x-HOLE_D/2, y-HOLE_D/2, HOLE_D, HOLE_D)
        for pt in PARTS:
            if hit(rect(pt), hr):
                bad.append((pt[0], f"hole@{x:g},{y:g}"))
    # MOD_HOLES are U2's own fixings and sit inside its footprint by design
    for pt in PARTS:
        rx, ry, w, h = rect(pt)
        inside = (ry >= LANE_H and rx >= BODY_X) or (ry + h <= LANE_H)
        if not (0 <= rx and rx + w <= W and 0 <= ry and ry + h <= H and inside):
            bad.append((pt[0], "OUTSIDE OUTLINE"))
    print(f"{f.relative_to(ROOT)}  ({W:g} x {H:g} mm, {len(PARTS)} parts)")
    print("  clean" if not bad else "")
    for a_, b_ in bad:
        print(f"  CLASH  {a_} <-> {b_}")

if __name__ == "__main__":
    raise SystemExit(main())
