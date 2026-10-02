# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A hardware design repo (not software): a camera-mounted, rechargeable ~6 V power pack for the Polaroid SX-70 that feeds the camera through two pogo pins on its base-plate contacts. Design v0.4, **nothing built or measured yet**. Most of the content is design reasoning in Markdown; the Python scripts generate drawings and CAD from hard-coded geometry. There are no tests, linter, or package manifest.

Two architectures are carried in parallel — Option A (4× 1.5 V regulated AAA, no converter) and Option B (2S LiPo + IP2326 USB-C charger + regulator). The measured motor peak current (docs/testing.md) decides between them; don't collapse to one option without that data. Option B is the one with a carrier PCB, schematic and KiCad file.

## Commands

Python environment: `.venv/` (Python 3.13, gitignored), recreated with `/opt/homebrew/bin/python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt`. It has `solidpython2` (Python → OpenSCAD, imported as `solid2`), trimesh / numpy-stl for inspecting STLs, and numpy, scipy, shapely, pandas, plotly, matplotlib. The existing SVG and STL scripts need only the standard library; `build_kicad_pcb.py` still needs KiCad's own Python (below), not the venv.

All scripts are run from the repo root and write their outputs into the tracked tree. Generated files (SVGs, netlist, `.kicad_pcb`) are committed, so regenerate and commit them whenever you change a script.

```bash
python scripts/build_stl.py [--openscad PATH]   # hardware/enclosure/stl/{lipo,aaa4}_{base,lid}.stl (needs OpenSCAD)
python scripts/layout_svg.py                    # hardware/enclosure/layout-top-{lipo,aaa4}.svg + overlap report
python scripts/pcb_svg.py                       # hardware/bom/PCB1-carrier/pcb-layout.svg + outline/hole checks
python scripts/schematic_svg.py                 # hardware/bom/PCB1-carrier/{schematic.svg,netlist.txt}

# Must use KiCad's bundled Python (imports pcbnew):
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 \
    scripts/build_kicad_pcb.py                  # hardware/pcb/sx70_carrier.kicad_pcb (placement only, unrouted)
```

Single enclosure part: `openscad -D 'battery_option="lipo"' -D 'part="base"' -o out.stl hardware/enclosure/sx70_power_pack.scad`. `part` is `base|lid|both`; `battery_option` is `lipo|aaa4`.

The SVG scripts are pure stdlib. The overlap checks in `layout_svg.py` / `pcb_svg.py` compare **body rectangles only**. KiCad DRC compares courtyards, which are larger, and found 15 real overlaps the SVG check missed (docs/pcb.md §3b). Don't treat a clean SVG check as a clean layout.

## Geometry is duplicated by hand — keep it in sync

There is no shared parameter file. The same dimensions are hard-coded in several places, and changing one means updating the others:

- `hardware/enclosure/sx70_power_pack.scad`: the source of truth for the shell (walls, bosses, magnet pockets, pogo bores, `pogo_spacing`, per-option bay sizes).
- `scripts/layout_svg.py`: mirrors the SCAD shell parameters (comment says so) and adds *proposed* component positions that the SCAD doesn't define.
- `scripts/pcb_svg.py` and `scripts/build_kicad_pcb.py`: each has its own `PARTS` table for the carrier PCB (ref, position, size/footprint) plus board extent `80 × 44`, lane height and `BODY_X`. Keep those two tables matching each other.
- `docs/pcb.md`: placement tables and the height budget, which the scripts implement.
- `scripts/schematic_svg.py`: embeds the netlist text itself.

Watch the coordinate frames. The PCB scripts use **board-local** mm (origin at the board's bottom-left, y up; `build_kicad_pcb.py` flips y for KiCad). The placement table in docs/pcb.md §3 uses **shell-outer** coordinates. The two can't be compared directly.

Docs and scripts have drifted apart before. Option B used to show a Pololu regulator and a 1000 µF C1 in the docs after the scripts had already moved to the TPS630702 and C1a/C1b at 2 × 220 µF (the TPS630702 caps VOUT at 470 µF). The BOM CSVs and the netlist from `schematic_svg.py` are the most reliable record of which parts are current. When you change a part, update README, design.md (BOM table and changelog), pcb.md and the scripts together.

## Docs map

- `README.md`: status, settled vs open decisions, safety notes. Keep the "Where things stand" and "Open questions" sections current when decisions change.
- `docs/design.md`: full rationale and calculations, with a **Changelog** at the bottom. Add an entry there for design changes.
- `docs/testing.md`: the bench measurements that unblock everything (step 0: are the base-plate contacts a real power rail at all?).
- `docs/pcb.md`: carrier PCB constraints, placement, DRC findings, fab spec.
- `docs/flex-order.md` and `hardware/flex-lens/`: a separate side-track on replacement camera flex circuits, not the power pack. The lens-flex KiCad project is deliberately not generated; it's meant to be created in the KiCad GUI.
- `hardware/bom/`: per-option BOM CSVs plus `digikey-order.csv` (consolidated order). Each `<ref>-<part>/` directory holds saved vendor evidence and a `notes.md` that separates *verified* from *assumed*. Save the material rather than linking to it, because listings change.

## Conventions

- Hard constraints to respect in any geometry change: camera bottom is **95 mm max** along the pack's long axis, pogo spacing **~50 mm** (provisional), pin stroke 0.7 mm, PCB standoff 2.6 mm to set 1.0 mm pin protrusion.
- Mark placeholders and unmeasured values explicitly; the docs consistently separate measured, datasheet-sourced and assumed numbers.
- `private/` (gitignored) holds order numbers, prices and vendor correspondence. Keep that kind of data out of tracked files. `offline-docs/` (gitignored) has local KiCad and OpenSCAD manuals for reference.
