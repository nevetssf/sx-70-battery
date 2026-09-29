#!/usr/bin/env python3
"""Build the carrier PCB (outline, mounting holes, footprint placement) in KiCad.

Run with KiCad's bundled Python:
  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 \
      scripts/build_kicad_pcb.py

Geometry comes from docs/pcb.md. Board-local origin is bottom-left, y up;
KiCad y is flipped here. Placement only — nothing is routed.
"""
import os, sys
import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "hardware", "pcb")
OUT = os.path.join(OUTDIR, "sx70_carrier.kicad_pcb")
KP = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"

BW, BH, LANE, BODY_X = 80.0, 44.0, 10.0, 43.0
OX, OY = 100.0, 60.0                       # board origin on the KiCad page

def P(x, y):                               # board-local mm -> KiCad point
    return pcbnew.VECTOR2I(pcbnew.FromMM(OX + x), pcbnew.FromMM(OY + (BH - y)))

# ref, lib, footprint, (x, y), rot, value
PARTS = [
    ("P1a", "TestPoint", "TestPoint_Pad_D2.0mm", (18.0, 7.0), 0, "pogo 7982-1"),
    ("P1b", "TestPoint", "TestPoint_Pad_D2.0mm", (68.0, 7.0), 0, "pogo 7982-1"),
    ("J3", "Connector_JST", "JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical", (10.5, 6.0), 0, "balance"),
    ("J2", "Connector_JST", "JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical", (25.0, 7.3), 0, "pack in"),
    ("SW1", "Connector_PinHeader_2.54mm", "PinHeader_1x03_P2.54mm_Vertical", (24.5, 2.2), 0, "SPDT slide"),
    ("C1a", "Capacitor_SMD", "CP_Elec_6.3x5.3", (33.0, 5.0), 0, "220uF"),
    ("C1b", "Capacitor_SMD", "CP_Elec_6.3x5.3", (42.0, 5.0), 0, "220uF"),
    ("D1", "Diode_SMD", "D_SMC", (49.0, 5.0), 0, "SS34"),
    ("R1", "Resistor_SMD", "R_2512_6332Metric", (56.0, 5.0), 0, "0R33 1W"),
    ("F1", "Fuse", "Fuse_1812_4532Metric", (61.5, 5.0), 0, "1812L075"),
    ("J4", "Connector_PinHeader_2.54mm", "PinHeader_1x05_P2.54mm_Vertical", (75.0, 6.0), 90, "U2 link"),
    ("U3", "Package_DFN_QFN", "DHVQFN-14-1EP_2.5x3mm_P0.5mm_EP1x1.5mm", (47.0, 36.0), 0, "TPS630702"),
    ("L1", "Inductor_SMD", "L_Coilcraft_XxL4020", (52.0, 36.0), 0, "1.5uH"),
    ("C2", "Capacitor_SMD", "C_0805_2012Metric", (57.0, 33.0), 0, "22uF"),
    ("C3", "Capacitor_SMD", "C_0805_2012Metric", (59.5, 33.0), 0, "22uF"),
    ("C4", "Capacitor_SMD", "C_0805_2012Metric", (62.0, 33.0), 0, "22uF"),
    ("C5", "Capacitor_SMD", "C_0805_2012Metric", (48.0, 40.0), 0, "10uF"),
    ("C6", "Capacitor_SMD", "C_0805_2012Metric", (50.5, 40.0), 0, "10uF"),
    ("R2", "Resistor_SMD", "R_0603_1608Metric", (47.0, 31.5), 0, "649k"),
    ("R3", "Resistor_SMD", "R_0603_1608Metric", (49.5, 31.5), 0, "100k"),
    ("Q1", "Package_TO_SOT_SMD", "SOT-23", (56.0, 40.0), 0, "2N7002"),
    ("R4", "Resistor_SMD", "R_0603_1608Metric", (61.0, 40.0), 0, "100k"),
    ("R5", "Resistor_SMD", "R_0603_1608Metric", (63.5, 40.0), 0, "100k"),
    ("R6", "Resistor_SMD", "R_0603_1608Metric", (68.0, 40.0), 0, "698k"),
    ("R7", "Resistor_SMD", "R_0603_1608Metric", (70.5, 40.0), 0, "100k"),
    ("C7", "Capacitor_SMD", "C_0603_1608Metric", (44.5, 33.0), 0, "100nF"),
]
PCB_HOLES = [("H1", 3.0, 3.0), ("H2", 77.0, 3.0), ("H3", 45.5, 41.5), ("H4", 77.0, 41.5)]
MOD_HOLES = [("H5", 51.0, 13.0), ("H6", 78.0, 13.0), ("H7", 51.0, 27.0), ("H8", 78.0, 27.0)]

def seg(board, p1, p2, layer, width=0.15):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(p1); s.SetEnd(p2)
    s.SetLayer(layer); s.SetWidth(pcbnew.FromMM(width))
    board.Add(s)

def text(board, x, y, s, size=1.0, layer=None):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(s); t.SetPosition(P(x, y))
    t.SetLayer(layer if layer is not None else pcbnew.F_SilkS)
    t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
    t.SetTextThickness(pcbnew.FromMM(size * 0.15))
    board.Add(t)

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    board = pcbnew.CreateEmptyBoard()
    # GetLayerID(name) returns -1 for the technical layers on a bare board,
    # which silently writes items to UNDEFINED and makes the file unloadable.
    edge, silk, cmt = pcbnew.Edge_Cuts, pcbnew.F_SilkS, pcbnew.Cmts_User

    # L-shaped outline
    pts = [(0,0),(BW,0),(BW,BH),(BODY_X,BH),(BODY_X,LANE),(0,LANE)]
    for i in range(len(pts)):
        seg(board, P(*pts[i]), P(*pts[(i+1) % len(pts)]), edge, 0.15)

    # zone annotations
    seg(board, P(0, LANE), P(BW, LANE), cmt, 0.1)
    text(board, 1.5, LANE - 2.2, "LANE - pogo pins + output path, no tall parts", 1.0, cmt)
    text(board, 1.5, BH - 2.0, "PCB1 carrier  80 x 44  2-layer  see docs/pcb.md", 1.2, cmt)

    missing, placed = [], 0
    for ref, lib, fp, (x, y), rot, val in PARTS:
        path = os.path.join(KP, lib + ".pretty")
        mod = pcbnew.FootprintLoad(path, fp) if os.path.isdir(path) else None
        if mod is None:
            missing.append((ref, lib, fp))
            text(board, x - 2, y, ref + " ?", 1.0, silk)
            continue
        mod.SetReference(ref); mod.SetValue(val)
        mod.SetPosition(P(x, y))
        if rot: mod.SetOrientationDegrees(rot)
        board.Add(mod); placed += 1

    for name, holes in (("board", PCB_HOLES), ("module", MOD_HOLES)):
        for ref, x, y in holes:
            mh = pcbnew.FootprintLoad(os.path.join(KP, "MountingHole.pretty"), "MountingHole_2.2mm_M2")
            mh.SetReference(ref); mh.SetValue("M2 " + name)
            mh.SetPosition(P(x, y)); board.Add(mh); placed += 1

    # U2 module keep-out footprint outline, 31 x 18 centred on (64.5, 20)
    mx0, my0, mx1, my1 = 64.5-15.5, 20-9, 64.5+15.5, 20+9
    for p1, p2 in (((mx0,my0),(mx1,my0)), ((mx1,my0),(mx1,my1)), ((mx1,my1),(mx0,my1)), ((mx0,my1),(mx0,my0))):
        seg(board, P(*p1), P(*p2), cmt, 0.2)
    text(board, mx0 + 1.5, my1 - 2.5, "U2 IP2326 module on standoffs (31 x 18)", 1.0, cmt)

    pcbnew.SaveBoard(OUT, board)
    print(f"wrote {os.path.relpath(OUT, ROOT)}  ({placed} footprints placed)")
    for ref, lib, fp in missing:
        print(f"  MISSING  {ref}: {lib}/{fp}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
