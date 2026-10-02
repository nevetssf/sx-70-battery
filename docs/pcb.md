# Carrier PCB — PCB1

Single 2-layer board carrying the pogo pins, the output path (C1, D1, R1), the switch, the battery connectors, the IP2326 module and the TPS630702 regulator. Only the cells and the 2S protection board stay off-board on wires.

**Status: placed, not routed.** `hardware/pcb/sx70_carrier.kicad_pcb` is generated from [scripts/build_kicad_pcb.py](../scripts/build_kicad_pcb.py), with outline, holes and footprints but no netlist or copper. KiCad DRC found the placement does not fit as drawn; see [§3b](#3b-kicad-project--and-what-drc-found) before relying on any position below.

---

## 1. Constraints that set the shape

| Constraint | Value | Source |
|---|---|---|
| Camera bottom max width | **95 mm** | Measured. The pack's long axis must fit inside this |
| Pogo pin spacing | **~50 mm** | Provisional — to be confirmed on the next camera opened |
| Pin protrusion | 1.0 mm past the outer face | Set by the 2.6 mm PCB standoff |
| Pin stroke | 0.7 mm | Mill-Max 7982-1 datasheet |

**The 50 mm spacing is what drives the architecture.** It is larger than the old 46 mm electronics bay, so the pins cannot both live in it. They have to be placed against the whole shell, which puts one of them under the battery region — hence the L-shaped board below.

It also kills the idea of lengthening the shell to ~105 mm to make room: 95 mm is the ceiling. (The pack was 92 mm before the TPS630702 replaced the Pololu module; it is 86 mm now.) The *other* axis runs along the camera's ~170 mm length and can grow freely, which is where the extra width comes from.

---

## 2. Shape and why

An **L**: a full-length **lane** along one edge carrying both pogo pins and the output-path parts, plus a **main body** under the IP2326 module and the regulator.

```
 y (mm, shell outer coords)                       outer 86 x 50 x 17.7
 47 +------------------------------------------------+ PCB
    |                    |  main body x 46-83          |
    |   battery sits on  |  +-------------------------+|
    |   the CASE FLOOR   |  | TPS630702 |   IP2326    ||
    |   beside the PCB   |  +-------------------------+|
 13 +--------------------+-----------------------------+
    | J3 P1a SW1/J2 C1a C1b D1 R1 F1  P1b  J4          |  <- lane, y 3-13
  3 +--------------------------------------------------+
    3                                                83   x
```

The lane sits at PCB height (2.6–4.2 mm above the inner floor). The battery does **not** stack on the board — it sits on the case floor beside the main body, which is what keeps the pack thin. That is the whole reason for the L.

**C1 (C1a + C1b) lives in the lane between the two pins on purpose.** Its job is supplying motor inrush; putting it in the passive column on the far side of the board would have added exactly the loop inductance that defeats it.

---

## 3. Placement

Shell outer **86 × 50 mm**, cavity 82 × 46, PCB inset 1 mm from the cavity. Coordinates are shell outer, origin at the outside corner — board-local positions in the scripts + 3 mm. This is the placement DRC rejected (§3b).

| Ref | Part | Centre (x, y) | Footprint | Notes |
|---|---|---|---|---|
| P1a | Mill-Max 7982-1 pogo | **21, 10** | 2.1 dia | **Underside mount**, soldertail up through the board |
| P1b | Mill-Max 7982-1 pogo | **71, 10** | 2.1 dia | 50 mm from P1a. Both shifted 3 mm right of centre so J3 and a mounting hole fit at the lane's left end |
| C1a, C1b | 220 µF 10 V polymer (440 µF total) | 36, 8 and 45, 8 | 6.3 dia can | Between the pins — shortest inrush loop. TPS630702 allows 470 µF max on VOUT |
| D1 | SS34 | 52, 8 | SMC | DO-214AB |
| R1 | Power resistor | 59, 8 | 2512 | Value from bench data |
| F1 | Littelfuse 1812L075 PPTC | 64.5, 8 | 1812 | After R1, before P1a |
| SW1 | SPDT slide | 27.5, 5 | 7 × 4 | Actuator faces the −y wall |
| **J2** | **Pack power in, JST-XH 2-pin** | **28, 10** | 8 × 6 | From the protection board's P+/P−, **not** the cells. ~2 A |
| **J3** | **Balance tap, JST-XH 3-pin** | **13.5, 9** | 11 × 6 | B−, midpoint, B+. Midpoint feeds the IP2326 **BM** pad |
| J4 | 5-way link to U2 | 78, 9 | 1×5 2.54 mm | |
| U2 | IP2326 module | 67.5, 23 | **31 × 18** | Measured from vendor drawing. USB-C faces the +x end wall |
| U3 | TPS630702 buck-boost block | ~55.5, 40 | ~15 × 12 | QFN + L1 + Cin/Cout + FB divider, on-board. Replaces the $35 Pololu module. IC itself at 50, 39 |
| — | Battery, on the **case floor** | 21.5, 29 | 35 × 26 | Not on the board |

PCB outline: lane `x 3–83, y 3–13`; main body `x 46–83, y 13–47`. Radius the internal corner at (46, 13) — it is a stress riser otherwise.

[scripts/layout_svg.py](../scripts/layout_svg.py) finds no part body fouling a lid-screw boss, a magnet pocket or another part. It compares body rectangles only; courtyards do overlap (§3b). Parts on the board clear the 1.5 mm magnet pads because the 2.6 mm standoff passes over them.

### Why the pins mount on the underside

The plungers point down through the case floor. Body on the bottom face, soldertail up through a hole, soldered on top. The body then extends 5.2 mm below the board: from 2.6 mm above the floor down to 1.0 mm past the outer face. That is exactly the protrusion target.

**Confirm the soldertail hole size from the 7982-1 datasheet before drawing the footprint.** The related 0906 series uses a 0.020″ (0.51 mm) mounting hole; do not assume it carries over.

### Height budget

| | mm |
|---|---|
| Case floor | 1.6 |
| Standoff to PCB underside | 2.6 |
| PCB | 1.6 |
| Tallest part (allowance) | 10.0 |
| **Total** | **15.8** |
| Interior ceiling | 16.1 |

0.3 mm of headroom. The 10 mm allowance was set by the old 1000 µF C1. The 6.3 × 5.3 mm cans of C1a/C1b no longer set it, so **check the real height of the tallest part — the vertical JST-XH headers and U2 on its standoffs — against it before ordering.**

---

## 3a. Board-level layout

Plan view: **[../hardware/bom/PCB1-carrier/pcb-layout.svg](../hardware/bom/PCB1-carrier/pcb-layout.svg)**, generated by [scripts/pcb_svg.py](../scripts/pcb_svg.py). That script finds no body, hole or outline clashes, but KiCad's courtyard check does (§3b).

Board is **80 × 44 mm**, L-shaped, origin bottom-left, inset 1 mm from the cavity — so board-local + 3 mm = shell coordinates.

### Headers and connectors

| Ref | Type | Goes to |
|---|---|---|
| **J2** | JST-XH 2-pin | Pack power, from U1 protection board `P+`/`P−` |
| **J3** | JST-XH 3-pin | Balance tap: `B−`, midpoint, `B+`. Midpoint feeds U2's `BM` |
| **J4** | 5-way link | The IP2326 module: `VIN+`, `GND`, `B+`, `B−`, `BM` |
| SW1 | SPDT slide | In series with the R6/R7 top leg, so off also removes the 9.3 µA divider draw |

There is deliberately **no output connector** — the pogo pins are the output, and J1 was dropped.

### Zones

- **Lane, y 0–10, full length.** Both pogo pins, C1a/C1b, D1, R1, F1, plus J2, J3, SW1 and J4. Nothing tall, because the battery passes over it in the shell.
- **Main body, x 43–80, y 10–44.** U2 on standoffs over its four dashed mounting holes, and the regulator block: U3, L1, Cin, Cout, the FB divider, and the three signal additions — Q1, the interlock divider and the EN undervoltage divider.

Four M2 holes at (3, 3), (77, 3), (45.5, 41.5), (77, 41.5) carry the board on 2.6 mm standoffs.

---

## 3b. KiCad project — and what DRC found

`hardware/pcb/sx70_carrier.kicad_pcb`, generated by [scripts/build_kicad_pcb.py](../scripts/build_kicad_pcb.py) using KiCad 10's bundled `pcbnew`. Outline, mounting holes and 34 footprints placed; nothing routed, no netlist yet. It loads cleanly and renders to `sx70_carrier-top.svg`.

**DRC reports 15 courtyard overlaps, and they are real.** The SVG checker in `scripts/layout_svg.py` compares component *body* rectangles. KiCad compares **courtyards**, which include pad extents and clearance and are materially larger. The placement that looked clean is not.

Overlapping pairs: C1a/C1b, C1a/J2, J2/SW1, J3/P1a, C1b/D1, D1/R1, F1/R1, H2/J4, C5/H3, plus the 0603 pairs at 2.5 mm pitch (R2/R3, R4/R5, R6/R7, C5/C6, C2/C3/C4).

**The lane is over-subscribed.** Summing courtyard widths for everything currently in it — J3, P1a, SW1, J2, C1a, C1b, D1, R1, F1, P1b, J4 — comes to roughly 81 mm before gaps, on an 80 mm board. It does not fit, and no amount of nudging fixes that.

**The fix is structural, not cosmetic:**

- **Keep only the output path in the lane**: P1a, C1a, C1b, D1, R1, F1, P1b.
- **Move the connectors into the main body**: J2, J3, J4 and SW1. SW1 can take the main body's +y edge, which is also a shell wall, so the actuator still reaches.
- **Widen the lane** from 10 mm to about 13 mm for the electrolytics plus courtyard.
- **Space 0603 pairs at 3.5 mm**, not 2.5 mm.

**This reopens the board size.** The main body is already carrying U2 at 31 × 18 plus the regulator block, so absorbing four connectors needs more area. There is 9 mm of length headroom before the 95 mm camera limit, and width is comparatively free — but the 86 × 50 figure will grow. Decide how much to give back before re-placing.

Smaller footprints would claw some of it back: a 220 µF polymer in a 7343 D-case instead of a 6.3 mm can, and 0402 for the dividers.

Other DRC output is expected at this stage: clearance and solder-mask items come from every pad sitting on no net, and resolve once a netlist is imported.

---

## 4. Nets and copper

Peak is ~2 A. IPC-2221 for external 1 oz copper at 10 °C rise gives ~0.75 mm for 2 A; specify **1.5 mm minimum** on the power path for margin, and pour where possible.

| Net | Path | Width |
|---|---|---|
| VBAT+ | **J2** → U3 VIN, and U2 charge return | 1.5 mm (~2 A in) |
| BM | **J3** centre pin → U2 BM pad | 0.5 mm |
| VOUT → V6 | U3 VOUT → C1a/C1b → D1 → R1 → F1 → **P1a** | **1.5 mm min, pour preferred** |
| GND | pour both layers, stitched | pour → **P1b** |
| CHG | USB-C → U2 → protection → cells, BM to midpoint | 1.0 mm |
| EN | SW1 → R6/R7 divider → U3 EN (Q1 pulls low on USB) | 0.3 mm |

- **C1a/C1b go as close to the pins as routing allows.** Its job is motor inrush; distance defeats it.
- **R1 is in series with the pins.** The pins add 40 mΩ of their own and F1 adds its hold resistance — measure in circuit and subtract both before choosing R1.
- Keep the V6 run from R1 through F1 to P1a short and fat. Everything in that path is source impedance you did not intend.

---

## 5. Fab

| | |
|---|---|
| Layers | 2 |
| Thickness | 1.6 mm |
| Copper | 1 oz |
| Finish | ENIG (gold pads under the pogo solder joints) |
| Min trace/space | 0.2 / 0.2 mm — inside PCBWay's standard 2-layer capability |
| Min hole | 0.3 mm |
| Outline | L-shape per above; radius the internal corner to avoid a stress riser |
| Vendor | PCBWay, same account as the flex orders |

---

## 5a. Battery connections

The pack needs **two** connections to the board, not one.

- **J2 — pack power.** From the 2S protection board's **P+/P−**, never straight off the cells, so the BMS guards both charge and discharge. Carries ~2 A.
- **J3 — balance tap.** The 3-wire balance lead: B−, midpoint, B+. The **midpoint feeds the IP2326's BM pad**, which is the only thing doing any cell balancing — the protection board does not balance. Bringing the whole lead to a standard JST-XH 3-pin also keeps the recovery path: a hobby charger can top-balance a drifted pack or set a 3.8 V/cell storage charge far faster than BM will.

**Connector current rating is a real constraint here.** JST-PH is rated 2 A, and the pack path draws ~2 A — right at the limit. JST-XH is rated 3 A in the same rough size, so both J2 and J3 use XH.

Note J3 taps the cells ahead of the protection board, as balance leads always do — an external charger plugged in there bypasses the BMS. That is normal hobby practice, but it is worth knowing before handing the connector to someone else.

---

## 6. Open

- [ ] **Confirm the 50 mm pin spacing** on the next camera opened. Every dimension here follows from it.
- [ ] Soldertail hole diameter for 7982-1, from the datasheet.
- [ ] Module attachment: headers or castellated pads. Headers cost height the budget has little of.
- [ ] SW1 actuator reach across the 1 mm board-to-wall gap plus the 2 mm wall.
- [ ] Does Option A need D1 too? Same rail, same backfeed case — see the README.
- [ ] R1 final value, after the shunt measurement.
