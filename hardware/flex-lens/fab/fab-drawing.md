# Fabrication Drawing — Lens / Shutter Flex

The fab drawing is where flex orders succeed or fail. Gerbers describe copper; they say nothing about coverlay, stiffeners, bend zones or copper type, and **all of those are quoted and built from the drawing.** Export it as a PDF alongside the Gerbers.

## Drawing checklist

- [ ] Overall dimensions, with tolerances (±0.1 mm on outline is typical; tighten only where it matters)
- [ ] Stackup cross-section: base PI, copper, coverlay, adhesive — with thicknesses
- [ ] Stiffener outlines, dimensioned, with material and thickness called out per location
- [ ] Coverlay openings (state that `F.Mask`/`B.Mask` in the Gerbers *are* the coverlay openings)
- [ ] Bend zones hatched, with bend axis and minimum bend radius for each
- [ ] Copper type callout — RA vs ED
- [ ] Surface finish
- [ ] Any gold-finger or sliding-contact areas, with plating spec
- [ ] Layer-to-outline registration datum
- [ ] Revision, date, part name, camera body it fits

## Notes block — paste onto the drawing

Edit the bracketed values once the design is measured.

```
NOTES:

1.  MATERIAL: POLYIMIDE FLEX, [1] LAYER, FINISHED THICKNESS [0.12] mm.
2.  COPPER: [0.5] oz, ROLLED ANNEALED (RA). ED COPPER IS NOT ACCEPTABLE —
    THIS PART IS FOLDED IN SERVICE.
3.  COVERLAY: POLYIMIDE, BOTH SIDES UNLESS NOTED. THE SOLDERMASK LAYERS IN
    THE SUPPLIED GERBERS DEFINE THE COVERLAY OPENINGS.
4.  SURFACE FINISH: ENIG.
5.  STIFFENER: [FR4 / POLYIMIDE], [0.2] mm, LOCATIONS PER DRAWING, BONDED
    TO THE [BOTTOM] SIDE.
6.  BEND ZONES ARE HATCHED. MINIMUM BEND RADIUS [1.2] mm.
    NO PLATED HOLES OR VIAS PERMITTED IN BEND ZONES.
    COPPER IS SINGLE-LAYER THROUGH ALL BEND ZONES.
7.  OUTLINE PROFILED PER EDGE.CUTS LAYER. OUTLINE TOLERANCE ±0.1 mm.
8.  NO ADHESIVE SQUEEZE-OUT INTO COVERLAY OPENINGS OR BEND ZONES.
9.  PART SHIPS FLAT. DO NOT CREASE OR FOLD FOR PACKAGING.
10. SAMPLE FIT-CHECK ARTICLE REQUESTED BEFORE FULL RUN.
```

Note 9 is not boilerplate — a creased flex arrives pre-damaged, and it happens.

## PCBWay order comment — draft

Paste into the order notes. Flex orders get human review and an unfamiliar outline draws questions; answering them up front saves a round trip.

```
This is a replacement flexible circuit for a vintage camera (Polaroid SX-70
lens/shutter assembly), reverse-engineered from the original part.

Key points:
- The part is FOLDED IN SERVICE, not static. Please use rolled-annealed (RA)
  copper. Bend zones are marked on the fab drawing with a minimum radius.
- Coverlay openings are defined by the soldermask layers in the Gerbers.
- Stiffener locations, material and thickness are on the fab drawing.
- The outline is irregular by design — it follows the original part. Please
  profile exactly to the Edge.Cuts layer.

Please confirm before starting:
1. Minimum trace/space you can hold on this stackup.
2. That RA copper is available at the requested weight.
3. Achievable outline tolerance.

Happy to supply the original part scan if it helps.
```

## Pre-fab gate

**Laser-cut a paper test piece from the outline and check it fits the body before ordering copper.** Cheap, fast, and catches a scale error — which is the standard way a scan-traced part goes wrong.

## Spec sheet

Fill in, then mirror into the PCBWay quote form.

| Parameter | Value |
|---|---|
| Layers | |
| Base PI thickness | |
| Finished thickness | |
| Copper weight | |
| Copper type | RA (required — part folds) |
| Coverlay | Polyimide, colour: |
| Stiffener material / thickness | |
| Stiffener locations | |
| Surface finish | ENIG |
| Silkscreen | |
| Outline tolerance | |
| Min bend radius | |
| Quantity | |
