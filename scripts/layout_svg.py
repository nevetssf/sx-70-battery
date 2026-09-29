#!/usr/bin/env python3
"""Scale top-down layout drawing of the power pack, from the SCAD parameters.

Draws the shell features (walls, divider, lid-screw bosses, magnet pockets,
pogo bosses, wall cutouts) and overlays the component footprints, then reports
any component that overlaps a floor obstruction.

Usage:  python scripts/layout_svg.py
Output: hardware/enclosure/layout-top-<option>.svg
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "hardware" / "enclosure"
SCALE, MARGIN = 5.0, 60.0

# ---- shell parameters, mirroring sx70_power_pack.scad ----
WALL, FLOOR_T, LID_T, DIVIDER_T, CORNER_R = 2.0, 1.6, 1.6, 1.2, 3.0
INSERT_D = 3.4
BOSS_D = INSERT_D + 3.0
MAG_D, MAG_T, MAG_FIT, MAG_BACK, MAG_WALL = 6.0, 2.0, 0.15, 0.8, 2.0
POGO_D, POGO_WALL, POGO_PAD_H, POGO_SPACING = 2.1, 2.5, 2.5, 50.0
POGO_LANE = 8.0        # pin centreline, in from the inner wall
CAMERA_MAX_W = 95.0
POGO_BOSS = False      # pins held by the carrier PCB, not a printed boss
PCB_STANDOFF = 2.6
POGO_ABOVE, POGO_STROKE = 5.2, 0.7

OPTIONS = {
    "lipo": dict(inner_h=13.0, batt=36.0, elec=46.0, inner_w=46.0, divider=False),
    "aaa4": dict(inner_h=14.0, batt=48.0, elec=24.0, inner_w=48.0, divider=True),
}

# Component footprints: name, w, h, (cx, cy) in outer coords, zone, note.
# Positions are a PROPOSAL — the SCAD does not define them.
def components(o, g):
    div_x = WALL + g["batt"]
    ex0 = div_x + DIVIDER_T
    ow = g["inner_w"] + 2 * WALL
    ol = g["batt"] + DIVIDER_T + g["elec"] + 2 * WALL
    if o == "lipo":
        return [
            ("LiPo 2S 350mAh", 35.0, 26.0, (21.5, 27.0), "floor", "on case floor, beside PCB", True),
            ("IP2326", 31.0, 18.0, (67.5, 23.0), "pcb", "USB-C to +x wall", True),
            ("TPS63070 block", 15.0, 12.0, (55.5, 40.0), "pcb", "QFN + L + caps", True),
            ("C1", 10.0, 10.0, (40.0, 8.0), "pcb", "close to pins", True),
            ("D1", 5.0, 3.0, (50.0, 8.0), "pcb", "", True),
            ("R1", 6.0, 3.0, (58.0, 8.0), "pcb", "", True),
            ("SW1", 7.0, 4.0, (27.5, 5.0), "pcb", "actuator to -y wall", True),
            ("J2 pack", 8.0, 6.0, (28.0, 10.0), "pcb", "XH 2-pin, 3 A", True),
            ("J3 bal", 11.0, 6.0, (14.0, 8.0), "pcb", "XH 3-pin", True),
        ]
    return [
        ("4x AAA holder", 46.0, 46.0, (WALL + g["batt"] / 2, ow / 2), "batt", "", True),
        ("C1 1000uF", 10.0, 10.0, (ex0 + 8.0, WALL + 7.0), "elec", "on PCB", True),
        ("R1", 6.0, 3.0, (ex0 + 8.0, ow - WALL - 5.0), "elec", "on PCB", True),
    ]

def geom(o):
    g = OPTIONS[o]
    inner_l = g["batt"] + (DIVIDER_T if g["divider"] else 0.0) + g["elec"]
    ol, ow = inner_l + 2 * WALL, g["inner_w"] + 2 * WALL
    mag_pocket_d = MAG_D + 2 * MAG_FIT
    mag_pad_h = max(0.0, MAG_T + 0.3 + MAG_BACK - FLOOR_T)
    mag_pad_d = mag_pocket_d + 2 * MAG_WALL
    inset = mag_pad_d / 2 + 1.0
    pad_max = max(mag_pad_h, POGO_PAD_H if POGO_BOSS else 0.0)
    bo = BOSS_D / 2 - 0.6
    div_x = WALL + g["batt"]
    ex0 = div_x + DIVIDER_T
    pcx = ol / 2
    return dict(
        g=g, inner_l=inner_l, ol=ol, ow=ow, div_x=div_x, ex0=ex0,
        cav_h=g["inner_h"] + pad_max, base_h=FLOOR_T + g["inner_h"] + pad_max,
        mag_pocket_d=mag_pocket_d, mag_pad_d=mag_pad_d, mag_pad_h=mag_pad_h,
        bosses=[(WALL + bo, WALL + bo), (ol - WALL - bo, WALL + bo),
                (WALL + bo, ow - WALL - bo), (ol - WALL - bo, ow - WALL - bo)],
        mags=[(ol * 0.25, WALL + inset), (ol * 0.75, WALL + inset),
              (ol * 0.25, ow - WALL - inset), (ol * 0.75, ow - WALL - inset)],
        pogos=[(pcx - POGO_SPACING / 2, WALL + POGO_LANE),
               (pcx + POGO_SPACING / 2, WALL + POGO_LANE)],
        pogo_pad_d=POGO_D + 2 * POGO_WALL,
        pogo_stick=POGO_ABOVE - (FLOOR_T + POGO_PAD_H),
    )

def circ_rect_hit(cx, cy, r, rx, ry, rw, rh):
    nx = max(rx, min(cx, rx + rw))
    ny = max(ry, min(cy, ry + rh))
    return (cx - nx) ** 2 + (cy - ny) ** 2 < r * r

def rects_hit(a, b):
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah

def svg(o):
    G = geom(o)
    ol, ow = G["ol"], G["ow"]
    W = ol * SCALE + 2 * MARGIN
    H = ow * SCALE + 2 * MARGIN + 130
    def X(v): return MARGIN + v * SCALE
    def Y(v): return MARGIN + v * SCALE
    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
      f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="ui-sans-serif,system-ui,sans-serif">')
    a('<style>'
      '.lbl{font-size:9px;fill:#1a1a1a}.sm{font-size:7.5px;fill:#555}'
      '.ttl{font-size:15px;font-weight:600;fill:#111}'
      '.dim{font-size:8px;fill:#777}'
      '.shell{fill:#f4f2ee;stroke:#333;stroke-width:1.5}'
      '.cav{fill:#fff;stroke:#999;stroke-width:1}'
      '.div{fill:#ddd8cf;stroke:#666;stroke-width:.8}'
      '.boss{fill:#e8dcc0;stroke:#9a8748;stroke-width:.8}'
      '.mag{fill:#cfe0f0;stroke:#4a7ea8;stroke-width:.8}'
      '.pogo{fill:#ffe0a8;stroke:#c98a1a;stroke-width:.9}'
      '.comp{fill:#e9f3e5;stroke:#4a8a3a;stroke-width:1;fill-opacity:.75}'
      '.bad{fill:#ffdede;stroke:#c0392b;stroke-width:1.6;fill-opacity:.8}'
      '.cut{fill:#c0392b;stroke:none;fill-opacity:.85}'
      '</style>')
    a(f'<rect width="{W:.0f}" height="{H:.0f}" fill="#fff"/>')
    a(f'<text x="{MARGIN}" y="26" class="ttl">SX-70 power pack — top-down layout, option "{o}"</text>')
    a(f'<text x="{MARGIN}" y="42" class="sm">Outer {ol:.1f} x {ow:.1f} x {G["base_h"]+LID_T:.1f} mm  ·  '
      f'clear height above bosses {G["g"]["inner_h"]:.1f} mm  ·  1 mm = {SCALE:g} px  ·  lid removed, looking down</text>')
    # shell + cavity
    a(f'<rect x="{X(0):.1f}" y="{Y(0):.1f}" width="{ol*SCALE:.1f}" height="{ow*SCALE:.1f}" '
      f'rx="{CORNER_R*SCALE:.1f}" class="shell"/>')
    a(f'<rect x="{X(WALL):.1f}" y="{Y(WALL):.1f}" width="{G["inner_l"]*SCALE:.1f}" '
      f'height="{G["g"]["inner_w"]*SCALE:.1f}" class="cav"/>')
    a(f'<rect x="{X(G["div_x"]):.1f}" y="{Y(WALL):.1f}" width="{DIVIDER_T*SCALE:.1f}" '
      f'height="{G["g"]["inner_w"]*SCALE:.1f}" class="div"/>')
    # obstructions
    obs = []
    for (cx, cy) in G["bosses"]:
        a(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{BOSS_D/2*SCALE:.1f}" class="boss"/>')
        a(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{INSERT_D/2*SCALE:.1f}" fill="#fff" stroke="#9a7" stroke-width=".6"/>')
        obs.append(("lid boss/insert", cx, cy, BOSS_D / 2, 0.0))
    for (cx, cy) in G["mags"]:
        a(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{G["mag_pad_d"]/2*SCALE:.1f}" class="mag"/>')
        a(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{G["mag_pocket_d"]/2*SCALE:.1f}" fill="none" stroke="#2c5d80" stroke-width="1" stroke-dasharray="3 2"/>')
        obs.append((f"magnet pad ({G['mag_pad_h']:.1f} mm)", cx, cy, G["mag_pad_d"] / 2, G["mag_pad_h"]))
    for (cx, cy) in G["pogos"]:
        a(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{G["pogo_pad_d"]/2*SCALE:.1f}" class="pogo"/>')
        a(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{POGO_D/2*SCALE:.1f}" fill="#fff" stroke="#c98a1a" stroke-width="1"/>')
        a(f'<text x="{X(cx):.1f}" y="{Y(cy)-G["pogo_pad_d"]/2*SCALE-3:.1f}" class="sm" text-anchor="middle">pogo</text>')
        if POGO_BOSS:
            obs.append((f"pogo boss ({POGO_PAD_H:.1f} mm)", cx, cy, G["pogo_pad_d"] / 2, POGO_PAD_H))
    # wall cutouts
    if o == "lipo":
        a(f'<rect x="{X(ol-WALL):.1f}" y="{Y(WALL+9.0-9.6/2):.1f}" width="{WALL*SCALE:.1f}" height="{9.6*SCALE:.1f}" class="cut"/>')
        a(f'<text x="{X(ol)+6:.1f}" y="{Y(WALL+9.0):.1f}" class="sm">USB-C</text>')
    swx = G["ex0"] + 20.0
    a(f'<rect x="{X(swx-7.5/2):.1f}" y="{Y(0):.1f}" width="{7.5*SCALE:.1f}" height="{WALL*SCALE:.1f}" class="cut"/>')
    a(f'<text x="{X(swx):.1f}" y="{Y(0)-5:.1f}" class="sm" text-anchor="middle">switch</text>')
    # components
    hits, cleared, overlaps = [], [], []
    for (name, w, h, (cx, cy), zone, note, raised) in components(o, G["g"]):
        rx, ry = cx - w / 2, cy - h / 2
        bad, ok = [], []
        for (d, ox, oy, r, hgt) in obs:
            if not circ_rect_hit(ox, oy, r, rx, ry, w, h):
                continue
            (ok if (raised and hgt > 0) else bad).append(d)
        if bad:
            hits.append((name, bad))
        if ok:
            cleared.append((name, ok))
        a(f'<rect x="{X(rx):.1f}" y="{Y(ry):.1f}" width="{w*SCALE:.1f}" height="{h*SCALE:.1f}" '
          f'class="{"bad" if bad else "comp"}" rx="2"/>')
        a(f'<text x="{X(cx):.1f}" y="{Y(cy):.1f}" class="lbl" text-anchor="middle">{name}</text>')
        a(f'<text x="{X(cx):.1f}" y="{Y(cy)+11:.1f}" class="sm" text-anchor="middle">{w:g} x {h:g} mm</text>')
        if note:
            a(f'<text x="{X(cx):.1f}" y="{Y(cy)+21:.1f}" class="sm" text-anchor="middle">{note}</text>')
    # carrier PCB outline (L): lane across the full length + main body
    if o == "lipo":
        lx0, lx1 = WALL + 1, ol - WALL - 1
        ly0, ly1 = WALL + 1, WALL + 11
        mx0, my1 = WALL + 44, ow - WALL - 1
        pts = [(lx0, ly0), (lx1, ly0), (lx1, my1), (mx0, my1), (mx0, ly1), (lx0, ly1)]
        d = " ".join(f"{X(px):.1f},{Y(py):.1f}" for px, py in pts)
        a(f'<polygon points="{d}" fill="none" stroke="#7a4fd0" stroke-width="2" stroke-dasharray="6 3"/>')
        a(f'<text x="{X(lx0)+6:.1f}" y="{Y(ly1)-5:.1f}" class="sm" fill="#7a4fd0">PCB1 outline (L) — tongue carries the far pogo pin</text>')

    # component vs component, same zone (both sit at the same height)
    placed = [(n, cx - w / 2, cy - h / 2, w, h, z)
              for (n, w, h, (cx, cy), z, _no, _r) in components(o, G["g"])]
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            an, ax, ay, aw, ah, az = placed[i]
            bn, bx, by, bw, bh, bz = placed[j]
            if az == bz and rects_hit((ax, ay, aw, ah), (bx, by, bw, bh)):
                ox = min(ax + aw, bx + bw) - max(ax, bx)
                oy = min(ay + ah, by + bh) - max(ay, by)
                overlaps.append((an, bn, ox, oy))
                a(f'<rect x="{X(max(ax,bx)):.1f}" y="{Y(max(ay,by)):.1f}" '
                  f'width="{ox*SCALE:.1f}" height="{oy*SCALE:.1f}" '
                  f'fill="#c0392b" fill-opacity=".45" stroke="#c0392b" stroke-width="1.5"/>')

    # legend
    ly = MARGIN + ow * SCALE + 26
    items = [("#e8dcc0", "lid-screw boss + M2.5 insert"), ("#cfe0f0", "magnet pad (pocket dashed)"),
             ("#ffe0a8", "pogo boss + bore"), ("#e9f3e5", "component, clear"),
             ("#ffdede", "component, COLLIDES"), ("#c0392b", "wall cutout")]
    for i, (col, txt) in enumerate(items):
        cx = MARGIN + (i % 3) * 230
        cy = ly + (i // 3) * 20
        a(f'<rect x="{cx}" y="{cy-9}" width="13" height="13" fill="{col}" stroke="#555" stroke-width=".8"/>')
        a(f'<text x="{cx+19}" y="{cy+1}" class="sm">{txt}</text>')
    a(f'<text x="{MARGIN}" y="{ly+52:.0f}" class="sm">Pogo protrusion {G["pogo_stick"]:.1f} mm vs {POGO_STROKE} mm stroke  ·  '
      f'component positions are a PROPOSAL, not defined in the SCAD</text>')
    a('</svg>')
    return "\n".join(p), hits, cleared, overlaps, G

def main():
    for o in OPTIONS:
        doc, hits, cleared, overlaps, G = svg(o)
        f = OUT / f"layout-top-{o}.svg"
        f.write_text(doc, encoding="utf-8")
        print(f"\n{f.relative_to(ROOT)}  ({G['ol']:.1f} x {G['ow']:.1f} mm)")
        if not hits:
            print("  no blocking collisions")
        for name, bad in hits:
            print(f"  BLOCKING   {name}  <->  {', '.join(sorted(set(bad)))}")
        for an, bn, ox, oy in overlaps:
            print(f"  OVERLAP    {an} <-> {bn}  by {ox:.1f} x {oy:.1f} mm")
        for name, ok in cleared:
            print(f"  by design  {name} sits above {', '.join(sorted(set(ok)))}")

if __name__ == "__main__":
    main()
