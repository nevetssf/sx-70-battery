# Lens / Shutter Flex — Reverse-Engineering Workspace

Replacement for the SX-70 lens (lensboard/shutter) flex. There is **no open-source design for this one** — Cundari's board is the *body* flex, and PolaStudio's lens flex was sold out as of Sept 2026. So this is a scan-and-retrace job. Routes and order prep: [../../docs/flex-order.md](../../docs/flex-order.md).

```
scan/    Source scans of the original, plus the scale calibration record
kicad/   KiCad project (create it here — see below)
fab/     Fabrication drawing notes and the PCBWay submission package
```

## Before anything else

1. **Continuity-map the original**, then **scan it**, then store it flat. The substrate keeps degrading and the geometry is unrecoverable once it crumbles. See [scan/README.md](scan/README.md).
2. **Identify which regions actually move when the camera folds.** This is the single most important input to the design, because it decides copper type, bend radii and whether copper can exist on both layers in those zones. Fold and unfold the camera with the original in place and mark the moving areas on a printout of the scan.
3. Cross-check the 7-way flex pinout in [OpenSX70 — For Dummies part 2](https://opensx70.com/tutorials/opensx70-for-dummies-2/) against your own continuity map. The author flags some details as uncertain; trust your meter over the page.

## KiCad project

The `.kicad_pcb` / `.kicad_pro` files are deliberately not generated. Unlike the carrier PCB (built by `scripts/build_kicad_pcb.py`), this board is traced by hand from a scan, so there is nothing to script. Create the project with **File → New Project** into `kicad/`, then apply the settings below. `kicad/sx70_lens_flex.kicad_dru` is provided and will load into Board Setup → Custom Rules.

### Board Setup

| Setting | Value |
|---|---|
| Layers | Start **single-sided** if the original is. Only go 2-layer if the scan proves it |
| Board thickness | 0.12 mm (matches the reference body flex; adjust to your measurement) |
| Solder mask | Treat `F.Mask` / `B.Mask` as the **polyimide coverlay** openings. KiCad has no coverlay concept — say so on the fab drawing |
| Edge.Cuts | The profiled outline. Laser or die cut, so it must be exact and closed |
| User.1 | Stiffener outlines |
| User.2 | Bend areas and bend-axis lines |
| User.Drawings | Dimensions and fab notes |

### Design rules

Starting values, loaded from the `.kicad_dru`. **Confirm against PCBWay's live flex quote form before fabbing** — I have not verified their current flex minimums, and they differ from the rigid-PCB figures.

- Min track width: 0.15 mm general, 0.20 mm for anything carrying motor or solenoid current
- Min clearance: 0.15 mm
- Min track width in bend zones: 0.20 mm, and keep it constant across the bend

### Tracing the scan

KiCad 7+ places a bitmap directly on the board as a reference image — set its scale from the ruler in the scan, then draw copper over it. For the outline, trace to vector first and bring it in as DXF at 1:1 in millimetres, onto `Edge.Cuts`.

Do what Cundari did on the body flex: don't reproduce the original slavishly. Add anything useful while you're in there.

## Flex design rules that differ from rigid PCB

These are what make a flex survive. Most are invisible to DRC — they are on you.

**In bend areas:**

- **Copper on one layer only.** Copper stacked on both layers through a bend creates an I-beam that cracks. If the region bends, keep it single-layer.
- **No plated through-holes, no vias.** Ever.
- Traces cross the bend **perpendicular to the bend axis** — straight across the fold. Never run a trace parallel to the bend line inside the bend zone.
- **Constant trace width** through the bend. No pads, no width steps, no tear-drops mid-bend.
- **Hatched, not solid, copper pours.** Solid copper stiffens the zone and fatigues.

**Bend radius**, as a multiple of total thickness — at 0.12 mm:

| Use | Multiple | Minimum radius |
|---|---|---|
| Formed once on assembly | 6× | 0.72 mm |
| Folded occasionally (the camera folding) | 10–20× | 1.2–2.4 mm |
| Continuous flexing | 100× | 12 mm |

The camera's fold is the middle row. Specify **rolled-annealed (RA) copper** rather than electro-deposited — ED copper is fine for a static flex and cracks in one that folds. Ask for it explicitly; it is not always the default.

**Everywhere else:**

- Radius the outline corners. Sharp internal corners are tear-initiation points.
- Curved or 45° trace corners, never 90°.
- **Teardrops at every pad-to-trace junction** — the classic flex failure is the trace cracking right where it meets the pad.
- **Anchor pads** (small spurs under the coverlay) for isolated pads, which otherwise peel.
- Stiffeners under every connector and hand-solder pad area. Call out material, thickness and exact location on the drawing.
