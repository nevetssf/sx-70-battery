# Replacement Flex — PCBWay Order Prep

Why this lives in the battery project: it started as risk mitigation. The original plan soldered a pigtail onto the traces feeding the film-chamber battery contacts, and 50-year-old flex adhesive releases almost immediately under heat — bench 1-B lifted pads and traces on the first switch at 415 °C.

**As of v0.3 the pack uses pogo pins and solders nothing to the camera, so that risk is gone.** What remains is the ordinary problem: these flexes disintegrate with age and handling regardless. Parts are already ordered (below), so this is now insurance and a standing reference rather than a dependency of the battery project. Full background in the SX-70 Repair Notes, *Flex circuit and soldering* → *Disintegrating flex and replacement options*.

---

## 1. First gate: which flex, and which motor chip?

Nothing below can be decided without these two answers.

- **Body flex** — connects S3, S5, S6, S7, S8, S9, the battery and the lensboard, and carries the motor driver.
  - **Later style, DIP-8 MCM** (SN28648P, Polaroid p/n 705982): solved, see Route A.
  - **Early Model 1, TO-5 metal-can MCC**: Cundari's board is DIP-8. Either jumper the MCC connections to the matching flex pads, or upgrade to the DIP-8 chip using his [replacement motor control chip](https://www.pcbway.com/project/shareproject/Polaroid_SX70_Motor_Control_Chip_Replacement_8_pin_DIP_version_13df00a5.html).
- **Lens / shutter flex** — **no open-source design exists.** The only commercial source found is PolaStudio ($50, sold out as of Sept 2026). This one means Route C: reverse-engineering.

**Scan the failing flex at maximum resolution before any further handling**, whichever route you take. The substrate keeps degrading and the geometry is unrecoverable once it crumbles.

---

## 2. Route A — Cundari's open-source body flex (no document prep)

[Polaroid SX70 Body Flex](https://www.pcbway.com/project/shareproject/Polaroid_SX70_Body_Flex_1d4fced3.html), CC BY-SA. **Order directly from the share page — there is an Add to cart button and the Gerbers are downloadable (`SX70_Flex_2025-12-09.zip`).** You prepare nothing.

Its published build:

| Parameter | Value |
|---|---|
| Layers | 2 |
| Finished thickness | 0.12 mm |
| Copper weight | 0.5 oz |

Fits both Model 1 and alpha-style motor connectors. The designer's warning is worth repeating: **do not make hard creased folds** when bending it around the body, or the copper breaks.

**Ordered:** PCBWay order **YF1811100**, product **W1041470AS3P6**, file `SX70_Flex_2025-12-09.zip` (Cundari's published Gerbers). Passed review 16 Sept 2026, paid 18 Sept, shipped 21 Sept 2026. **Motor control chip replacement — ordered.** PCBWay order **YH1814072**, placed 22 Sept 2026 (23 Sept 12:03 PCBWay time, GMT+8):

| | |
|---|---|
| Line items | `W1041470AS3P8` — bare PCB, file `W832028AS2Y7_Gerber_PCB1_2026-04-01 (2).zip`<br>`T-3P9W1041470A (W1041470AS3P8)` — assembly |
| Quantity | **10 assembled boards** |
| Cost | **$134.79** — boards $25.44, components $21.35, assembly $88.00 |
| Quoted build time | 18–20 days |
| Rep | service12@pcbway.com (quote came via service33 / Ivy Yang) |

The earlier 5-unit quote (`T-3P5W1041470A`, $71.03) is superseded.

⚠️ **The build window overlaps the Chinese holidays.** The quote email linked PCBWay's *Holiday Schedule of Mid-Autumn Festival & National Day 2026*, and both fall inside an 18–20 day build starting 23 Sept. Check that schedule before assuming a mid-October delivery.

The quote carried a BOM spreadsheet attachment (`Quotation T-3P9W1041470A-10units-BOM_...xls`) — that is the only record of which components PCBWay is actually fitting. Worth saving into the repo alongside the board files.

**Pins are a separate order.** The board is 10 × 10 mm, 1.0 mm thick, with SMT parts on the board and **through-hole pins into the flex** — 5 pins, the DIP-8 pattern with 3 unpopulated, matching the original MCM's 5 populated legs. The [GitHub BOM](https://github.com/fotocundari/SX70-Motor-Control-Chip) specifies making them from the legs of **Stackpole JW60ZT0R00** tin-plated 0 Ω through-hole jumper resistors (22 AWG), stocked by Digi-Key and Mouser.

Two cautions: the PCBWay page's wording — "requires adding jumper wires to replace pins" — contradicts the GitHub BOM, which is the more specific and more recent source; and **check the PCBA quotation BOM before ordering pins separately**, since the $21.35 component line may already cover them.

**The build parameters were not captured anywhere.** PCBWay's notification emails list only the product number and filename, so the material, copper weight, thickness and finish for YF1811100 exist only on the order management page. Log in and record them in the table below before the order ages out — without them the build is not reproducible.

| Parameter | As built (fill from order page) |
|---|---|
| Layers | |
| Finished thickness | |
| Copper weight | |
| Copper type | |
| Coverlay | |
| Stiffener | |
| Surface finish | |
| Quantity | |

## 3. Route B — buy finished

[PolaStudio](https://polastudio.online/products/polaroid-sx70-sonar-680-electronic-flex-repair-tools): lens flex $50, body flex $100 (includes a new MCM). Both sold out as of Sept 2026; email about restock. No fabrication, no prep.

## 4. Route C — reverse-engineer an original

Required for the lens/shutter flex, optional for a body flex you want dimensionally identical to the original. The established workflow:

1. **Scan the original flat** at maximum optical resolution with a dimensional reference in frame. Do this first, before handling degrades it further.
2. **Trace to vector.** Corel was used in the OpenSX70 write-up; any vector tool works.
3. **Import into EDA** as DXF for the outline, then lay out copper against the scan.
4. **Laser-cut a paper test piece** and check fit in the body *before* spending money on fab.
5. **Fab at PCBWay.**

Worth doing what Cundari did: add pads for the Mabuchi motors repair shops fit, rather than reproducing the original exactly.

**Tooling note: KiCad is currently in this machine's Trash.** Reinstall before starting; it handles this fine.

---

## 5. PCBWay flex order parameters

Fill this in per order. Applies to Route C, and to changing the build options on Route A.

| Parameter | Value | Notes |
|---|---|---|
| Layers | | 1 or 2 |
| Base PI thickness | | PCBWay standard: 0.025 / 0.05 mm (1-layer), 0.08 mm (2-layer) |
| Finished thickness | | Cundari's body flex: 0.12 mm |
| Copper weight | | 0.25 oz (9 µm) up to 2 oz (70 µm); 0.5 oz on the reference design |
| Coverlay | | Polyimide coverlay, not LPI solder mask — specify colour and openings |
| Stiffener: material | | FR4, polyimide, or stainless steel |
| Stiffener: thickness | | FR4 offered 0.2 / 0.4 / 0.5 / 0.6 / 0.8 / 1.0 / 1.2 / 1.5 mm |
| Stiffener: locations | | **Call out on the fab drawing.** Needed under connector and solder-pad areas |
| Surface finish | | ENIG is the usual choice for flex |
| Silkscreen | | Optional legend |
| EMI shielding film | | Optional; not needed here |
| Outline / profiling | | Laser or die cut — the outline layer must be exact |
| Bend areas + min radius | | Annotate. No traces crossing a fold perpendicular if avoidable |
| Quantity | | |

**Confirm minimum trace/space and minimum hole size against PCBWay's live quote form** — I have not verified the current flex figures, and they differ from their rigid-PCB values.

### Materials PCBWay actually offers

Verified from their FPC stackup and flex capability pages, Sept 2026.

| Category | Options |
|---|---|
| Base | **Polyimide (PI)**, 12.5 µm (0.5 mil) to 125 µm (5 mil), with or without adhesive. Dk 3.5 adhesive / 3.3 adhesiveless. **PET (transparent)** also offered |
| Copper weight | Raw 9 / 12 / 18 / 35 / 50 / 70 / 88 µm; finished 15–88 µm. Flex portion 0.5–2 oz finished, 4 oz max |
| Copper type | **Not stated anywhere on their public pages — you must ask.** See below |
| Coverlay | Polyimide. Yellow (standard), black, white (thicker, 31–43 µm PI). 12.5–43 µm PI backing + 12.5–50 µm adhesive |
| Stiffener | PI, FR4 (0.2 / 0.4 / 0.5 / 0.6 / 0.8 / 1.0 / 1.2 / 1.5 mm), stainless steel. Thickness tol ±10% |
| Surface finish | HASL, **ENIG**, ENEPIG, electrolytic Ni/Au, soft gold, hard gold, immersion silver, immersion tin, OSP |
| Layers | Flex 1–12; rigid-flex up to 26 |
| Thickness tolerance | ±1.0 mil single-layer; ±1.2 mil multilayer up to 12 mil |
| Max order qty | 3000 |

Multilayer adhesiveless stackups use 13 µm "pure gum" spacers on inner layers.

**The copper-type gap matters.** PCBWay's public pages never distinguish rolled-annealed from electrodeposited, so the standard flex process gives you whatever is standard — and ED copper cracks in a part that folds. For any SX-70 flex, RA has to be requested explicitly and confirmed in writing. This applies to the body flex as much as the lens flex: Cundari's own warning is not to make hard creased folds when bending his board around the body.

## 6. Files to submit

- **Gerbers**, RS-274X, one per layer, including the board outline on its own layer.
- **Excellon drill** file, if there are any holes or vias.
- **Fabrication drawing (PDF)** — this is where flex orders are won or lost. It must show:
  - Overall dimensions and tolerances
  - Stackup: base PI, copper, coverlay, adhesive
  - Stiffener locations, materials and thicknesses
  - Coverlay openings
  - Bend areas and minimum bend radius
  - Surface finish and any gold-finger/contact plating
- A note in the order comments describing what the part is. Flex orders get human review, and an unusual outline draws questions.

---

## 7. Open

- [x] Which flex is being replaced — **lens / shutter**. Route C, workspace in [../hardware/flex-lens/](../hardware/flex-lens/).
- [ ] Which motor chip is in the target body — TO-5 MCC or DIP-8 MCM?
- [ ] Did the Sept 2026 PCBWay quote come back?
- [ ] Target camera confirmed (1-A / 1-B / 1-C / Model 2)?

---

## 8. Links

**Nick Cundari — designs used here**

- [Polaroid SX70 Body Flex (PCBWay)](https://www.pcbway.com/project/shareproject/Polaroid_SX70_Body_Flex_1d4fced3.html) — replacement body flex. Gerbers downloadable, orderable directly from the page. CC BY-SA
- [SX70 Motor Control Chip Replacement, 8-pin DIP (PCBWay)](https://www.pcbway.com/project/shareproject/Polaroid_SX70_Motor_Control_Chip_Replacement_8_pin_DIP_version_13df00a5.html) — SN28648P replacement, order page
- [GitHub — fotocundari/SX70-Motor-Control-Chip](https://github.com/fotocundari/SX70-Motor-Control-Chip) — source, Gerbers and BOM for the above. CC BY-SA 4.0. **This is where the pin spec lives**
- [GitHub — fotocundari/OpenSX70-ECM-Cundari](https://github.com/fotocundari/OpenSX70-ECM-Cundari) — his fork of the OpenSX70 ECM firmware, GPLv3

**PCBWay**

- [Flex / rigid-flex capabilities](https://www.pcbway.com/fpc-rigid-flex-pcb.html) — layer counts, copper weights, surface finishes
- [FPC stackup and materials](https://www.pcbway.com/pcb_prototype/Stack_up_for_FPC.html) — base PI thicknesses, coverlay, adhesive options
- Order management page — the **only** place the as-built parameters for YF1811100 exist

**Other sources**

- [OpenSX70 — The BodyFlex circuit](https://opensx70.com/posts/2020/19/bodyflex-1) — reverse-engineering route and body flex background
- [OpenSX70 — For Dummies part 2](https://opensx70.com/tutorials/opensx70-for-dummies-2/) — S2–S9 and the 7-way flex pinout (author flags some details as uncertain)
- [PolaStudio — SX70/Sonar/680 flex](https://polastudio.online/products/polaroid-sx70-sonar-680-electronic-flex-repair-tools) — commercial lens and body flex, sold out Sept 2026
