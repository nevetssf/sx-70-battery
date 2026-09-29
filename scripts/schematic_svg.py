#!/usr/bin/env python3
"""Schematic of the SX-70 power pack, Option B.

Emits an SVG drawing plus a plain-text netlist. Net labels are used instead of
long wires, so each block reads on its own.

Usage:  python scripts/schematic_svg.py
Output: hardware/bom/PCB1-carrier/schematic.svg
        hardware/bom/PCB1-carrier/netlist.txt
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "hardware" / "bom" / "PCB1-carrier"
W, H = 1580, 1000
d: list[str] = []
def a(s): d.append(s)

def wire(*pts, w=1.6):
    a('<polyline points="' + " ".join(f"{x},{y}" for x, y in pts) +
      f'" fill="none" stroke="#111" stroke-width="{w}"/>')
def dot(x, y): a(f'<circle cx="{x}" cy="{y}" r="3.4" fill="#111"/>')
def txt(x, y, s, c="lbl", anchor="start"):
    a(f'<text x="{x}" y="{y}" class="{c}" text-anchor="{anchor}">{s}</text>')
def box(x, y, w, h, ref, name, pins=(), fill="#eef4fb"):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="#111" stroke-width="1.8"/>')
    txt(x + w/2, y + 20, ref, "ref", "middle")
    txt(x + w/2, y + 36, name, "sub", "middle")
    for (px, py, t, side) in pins:
        txt(px, py, t, "pin", side)
def gnd(x, y):
    wire((x, y), (x, y + 14))
    for i, hw in enumerate((11, 7, 3)):
        a(f'<line x1="{x-hw}" y1="{y+14+i*5}" x2="{x+hw}" y2="{y+14+i*5}" stroke="#111" stroke-width="1.8"/>')
def netlabel(x, y, s, anchor="start"):
    w = 11 + len(s) * 7.6
    x0 = x if anchor == "start" else x - w
    a(f'<rect x="{x0}" y="{y-11}" width="{w}" height="21" rx="10" fill="#fff3cd" stroke="#b8860b" stroke-width="1.2"/>')
    txt(x0 + w/2, y + 5, s, "net", "middle")
def res(x, y, ref, val, vert=False):
    if vert:
        wire((x, y), (x, y+8)); a(f'<rect x="{x-9}" y="{y+8}" width="18" height="34" fill="#fff" stroke="#111" stroke-width="1.8"/>')
        wire((x, y+42), (x, y+50)); txt(x+15, y+22, ref, "ref"); txt(x+15, y+37, val, "sub")
    else:
        wire((x, y), (x+8, y)); a(f'<rect x="{x+8}" y="{y-9}" width="34" height="18" fill="#fff" stroke="#111" stroke-width="1.8"/>')
        wire((x+42, y), (x+50, y)); txt(x+25, y-15, ref, "ref", "middle"); txt(x+25, y+25, val, "sub", "middle")
def cap(x, y, ref, val):
    wire((x, y), (x, y+14))
    a(f'<line x1="{x-15}" y1="{y+14}" x2="{x+15}" y2="{y+14}" stroke="#111" stroke-width="2.4"/>')
    a(f'<line x1="{x-15}" y1="{y+22}" x2="{x+15}" y2="{y+22}" stroke="#111" stroke-width="2.4"/>')
    wire((x, y+22), (x, y+36)); txt(x+21, y+14, ref, "ref"); txt(x+21, y+29, val, "sub")
def diode(x, y, ref, val):
    wire((x, y), (x+10, y))
    a(f'<polygon points="{x+10},{y-11} {x+10},{y+11} {x+30},{y}" fill="#fff" stroke="#111" stroke-width="1.8"/>')
    a(f'<line x1="{x+30}" y1="{y-11}" x2="{x+30}" y2="{y+11}" stroke="#111" stroke-width="2.6"/>')
    wire((x+30, y), (x+40, y)); txt(x+20, y-19, ref, "ref", "middle"); txt(x+20, y+30, val, "sub", "middle")
def inductor(x, y, ref, val):
    wire((x, y), (x+8, y))
    a(f'<path d="M{x+8},{y} q7,-13 14,0 q7,-13 14,0 q7,-13 14,0" fill="none" stroke="#111" stroke-width="1.8"/>')
    wire((x+50, y), (x+58, y)); txt(x+29, y-17, ref, "ref", "middle"); txt(x+29, y+20, val, "sub", "middle")
def nmos(x, y, ref, val):
    a(f'<line x1="{x}" y1="{y-26}" x2="{x}" y2="{y+26}" stroke="#111" stroke-width="2.2"/>')
    a(f'<line x1="{x-16}" y1="{y}" x2="{x-4}" y2="{y}" stroke="#111" stroke-width="1.8"/>')
    a(f'<line x1="{x-4}" y1="{y-22}" x2="{x-4}" y2="{y+22}" stroke="#111" stroke-width="2.2"/>')
    wire((x, y-26), (x+22, y-26)); wire((x, y+26), (x+22, y+26))
    txt(x+27, y-22, ref, "ref"); txt(x+27, y-7, val, "sub")

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  f'font-family="ui-sans-serif,system-ui,sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>')
a('<style>.lbl{font-size:13px;fill:#111}.ref{font-size:13px;font-weight:600;fill:#111}'
  '.sub{font-size:11px;fill:#555}.pin{font-size:10px;fill:#333}.net{font-size:11px;font-weight:600;fill:#7a5c00}'
  '.ttl{font-size:20px;font-weight:600;fill:#111}.h{font-size:12px;font-weight:600;fill:#2c7bb6}'
  '.note{font-size:11px;fill:#444}</style>')
txt(40, 40, "SX-70 External Power Pack — Option B, carrier PCB", "ttl")
txt(40, 62, "Net labels connect blocks. Pogo pins are the only output; the pack is for i-Type film.", "note")

# ---- battery / protection ----
txt(40, 100, "PACK &amp; PROTECTION", "h")
box(40, 120, 120, 120, "BT1", "2S LiPo", [(52, 160, "B+", "start"), (52, 186, "BM", "start"), (52, 212, "B−", "start")], "#e8f6ea")
box(250, 120, 130, 120, "U1", "2S protection", [(262, 160, "B+", "start"), (262, 186, "BM", "start"), (262, 212, "B−", "start"),
                                                (368, 165, "P+", "end"), (368, 205, "P−", "end")], "#e8f6ea")
for i, yy in enumerate((160, 186, 212)):
    wire((160, yy), (250, yy))
box(120, 290, 120, 60, "J3", "XH-3 balance", [], "#d6ecff")
wire((180, 290), (180, 212)); dot(180, 212)
txt(120, 372, "B−, midpoint, B+ — midpoint also feeds U2 BM", "note")
wire((380, 165), (430, 165)); netlabel(432, 165, "VBAT")
wire((380, 205), (430, 205)); netlabel(432, 205, "GND")

# ---- charger ----
txt(560, 100, "CHARGER", "h")
box(560, 120, 150, 150, "U2", "IP2326 module", [(572, 158, "VIN+", "start"), (572, 182, "GND", "start"),
                                                (572, 212, "B+", "start"), (572, 236, "B−", "start"), (572, 260, "BM", "start")], "#e7d9f5")
box(560, 300, 150, 44, "J4", "5-way link to U2", [], "#d6ecff")
txt(560, 366, "USB-C is on the module. VIN+ is tapped for the interlock.", "note")
netlabel(500, 158, "VUSB", "end"); wire((500, 158), (560, 158))
netlabel(500, 212, "VBAT", "end"); wire((500, 212), (560, 212))
netlabel(500, 236, "GND", "end"); wire((500, 236), (560, 236))
netlabel(500, 260, "BM", "end"); wire((500, 260), (560, 260))

# ---- regulator ----
txt(830, 100, "REGULATOR", "h")
box(880, 130, 170, 230, "U3", "TPS630702", [
    (892, 168, "VIN", "start"), (892, 196, "EN", "start"), (892, 224, "PS/SYNC", "start"),
    (892, 252, "VSEL", "start"), (892, 280, "VAUX", "start"), (892, 330, "GND/PGND", "start"),
    (1038, 168, "L1", "end"), (1038, 196, "L2", "end"), (1038, 240, "VOUT", "end"),
    (1038, 280, "FB", "end"), (1038, 320, "FB2", "end")], "#ffd9d9")
netlabel(800, 168, "VBAT", "end"); wire((800, 168), (880, 168))
netlabel(800, 196, "EN", "end"); wire((800, 196), (880, 196))
wire((880, 224), (840, 224), (840, 168)); dot(840, 168)
txt(700, 240, "PS/SYNC high = power-save (PFM)", "note")
wire((880, 252), (856, 252), (856, 300)); gnd(856, 300)
cap(880 - 40, 280, "Cvaux", "100n"); wire((840, 280), (880, 280)); gnd(840, 316)
inductor(1060, 150, "L1", "1.5 µH")
wire((1050, 168), (1060, 168), (1060, 150)); wire((1118, 150), (1130, 150), (1130, 196), (1050, 196))
cap(820, 380, "Cin", "2×10 µF"); wire((820, 380), (820, 168)); dot(820, 168); gnd(820, 416)
wire((1050, 240), (1120, 240)); netlabel(1122, 240, "VOUT")
cap(1180, 290, "Cout", "3×22 µF"); wire((1180, 290), (1180, 240)); dot(1180, 240); gnd(1180, 326)
res(1090, 280, "R2", "649k"); wire((1050, 280), (1090, 280))
wire((1140, 280), (1160, 280), (1160, 240)); dot(1160, 240)
res(1090, 320, "R3", "100k", vert=False); wire((1050, 320), (1090, 320)); gnd(1140, 320)
txt(830, 420, "FB divider sets 5.99 V against the 0.8 V reference", "note")

# ---- control ----
txt(40, 470, "CONTROL — EN gating", "h")
box(40, 500, 120, 56, "SW1", "SPDT slide", [], "#d6ecff")
netlabel(180, 528, "VBAT", "end"); wire((160, 528), (180, 528))
res(240, 528, "R6", "698k"); wire((220, 528), (240, 528))
wire((290, 528), (330, 528)); dot(330, 528); netlabel(332, 528, "EN")
res(330, 580, "R7", "100k"); wire((330, 528), (330, 580)); gnd(380, 580)
nmos(520, 560, "Q1", "2N7002")
wire((520, 534), (520, 528), (400, 528)); dot(400, 528)
wire((542, 586), (560, 586)); gnd(560, 586)
res(420, 640, "R4", "100k"); wire((470, 640), (504, 640))
netlabel(400, 640, "VUSB", "end"); wire((400, 640), (420, 640))
res(560, 690, "R5", "100k", vert=False); wire((504, 640), (504, 690), (560, 690)); gnd(610, 690)
txt(40, 740, "EN high only when SW1 is on AND no USB present. SW1 is in series with R6 so", "note")
txt(40, 758, "switching off also removes the 9.3 µA divider draw. R6/R7 double as a ~6.4 V soft LVC.", "note")

# ---- output ----
txt(830, 470, "OUTPUT PATH", "h")
netlabel(830, 520, "VOUT", "end")
wire((830, 520), (860, 520))
cap(880, 520, "C1a/C1b", "2×220 µF"); wire((860, 520), (880, 520)); dot(880, 520); gnd(880, 556)
diode(930, 520, "D1", "SS34"); wire((880, 520), (930, 520))
res(990, 520, "R1", "0.22–0.47 Ω"); wire((970, 520), (990, 520))
a('<rect x="1070" y="504" width="52" height="32" fill="#fff" stroke="#111" stroke-width="1.8"/>')
a('<line x1="1070" y1="536" x2="1122" y2="504" stroke="#111" stroke-width="1.8"/>')
txt(1096, 496, "F1", "ref", "middle"); txt(1096, 552, "PTC 1812L075", "sub", "middle")
wire((1040, 520), (1070, 520)); wire((1122, 520), (1160, 520))
a('<circle cx="1180" cy="520" r="11" fill="#fff2b8" stroke="#b8860b" stroke-width="2"/>')
txt(1198, 516, "P1a", "ref"); txt(1198, 532, "pogo +", "sub")
a('<circle cx="1180" cy="600" r="11" fill="#fff2b8" stroke="#b8860b" stroke-width="2"/>')
txt(1198, 596, "P1b", "ref"); txt(1198, 612, "pogo −", "sub")
wire((1169, 600), (1140, 600)); gnd(1140, 600)
txt(830, 650, "C1 before D1/R1 so surge current still passes through R1.", "note")
txt(830, 668, "D1 blocks film → pack. F1 ends a sustained pack → film fault.", "note")
txt(830, 686, "R1 budget = target minus pogo pins (40 mΩ) minus F1 hold resistance.", "note")

txt(40, 830, "NOT ON THE BOARD: BT1, U1 and the USB-C connector (on the U2 module).", "note")
txt(40, 848, "NO output connector — J1 was dropped; the pogo pins are the output.", "note")
txt(40, 866, "U2 pads LED and NTC are unused. U3 PG and FB2 left open.", "note")
a('</svg>')

NET = """SX-70 External Power Pack — Option B — netlist
Generated by scripts/schematic_svg.py. Reference while drawing in an EDA tool.

COMPONENTS
  BT1   2S LiPo pack, 350-500 mAh          off-board
  U1    2S protection board, DW01/8205      off-board
  J3    JST-XH 3-pin, balance tap
  J2    JST-XH 2-pin, pack power in
  U2    IP2326 charger module (Z-6732-V4.0, 2S)   on standoffs
  J4    5-way link to U2
  U3    TPS630702, adjustable buck-boost
  L1    1.5 uH shielded
  Cin   2 x 10 uF / 25 V
  Cvaux 100 nF
  Cout  3 x 22 uF / 16 V
  R2    649 k 1%          FB divider upper
  R3    100 k 1%          FB divider lower
  C1a   220 uF 10 V polymer
  C1b   220 uF 10 V polymer
  D1    SS34 Schottky
  R1    0.22-0.47 ohm 1 W
  F1    Littelfuse 1812L075 PPTC
  SW1   SPDT slide
  R6    698 k 1%          EN divider upper / soft LVC
  R7    100 k 1%          EN divider lower
  Q1    2N7002 N-MOSFET
  R4    100 k             interlock divider upper
  R5    100 k             interlock divider lower
  P1a   Mill-Max 7982-1 pogo pin, output +
  P1b   Mill-Max 7982-1 pogo pin, output -

NETS
  VBAT    U1.P+  J2.1  U2.B+  U3.VIN  Cin.1  SW1.common
  GND     U1.P-  J2.2  U2.B-  U3.GND  U3.PGND  Cin.2  Cvaux.2  Cout.2
          C1a.2  C1b.2  R3.2  R5.2  R7.2  Q1.S  P1b
  BM      BT1.BM  U1.BM  J3.2  U2.BM
  VUSB    U2.VIN+  R4.1
  SW      SW1.throw  R6.1
  EN      R6.2  R7.1  Q1.D  U3.EN
  GATE    R4.2  R5.1  Q1.G
  SWNODE1 U3.L1  L1.1
  SWNODE2 U3.L2  L1.2
  VOUT    U3.VOUT  Cout.1  C1a.1  C1b.1  R2.1  D1.anode
  FB      R2.2  R3.1  U3.FB
  VAUX    U3.VAUX  Cvaux.1
  V6A     D1.cathode  R1.1
  V6B     R1.2  F1.1
  V6      F1.2  P1a

TIED / UNUSED
  U3.PS/SYNC -> VBAT     power-save (PFM) enabled
  U3.VSEL    -> GND      output scaling unused
  U3.FB2     open        per datasheet when unused
  U3.PG      open        optional power-good LED
  U2.LED, U2.NTC  unused

NOTES
  C1a/C1b sit on VOUT, before D1/R1, so surge current still passes through R1.
  Total VOUT capacitance must stay under 470 uF (TPS63070 datasheet).
  EN is high only when SW1 is on AND VUSB is absent.
  R6/R7 also form a ~6.4 V soft undervoltage lockout via the precise EN threshold.
  R1 final value = target source impedance minus pogo pins (40 mOhm) minus F1 hold resistance.
"""

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "schematic.svg").write_text("\n".join(d), encoding="utf-8")
(OUT / "netlist.txt").write_text(NET, encoding="utf-8")
print("wrote", (OUT / "schematic.svg").relative_to(ROOT))
print("wrote", (OUT / "netlist.txt").relative_to(ROOT))
