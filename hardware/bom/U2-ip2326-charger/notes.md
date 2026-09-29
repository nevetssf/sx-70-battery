# U2 — IP2326 USB-C 2S charger module

**Buy: the purple 2S board, `Z-6732-V4.0`.** ~$2.20 each at 10 off (AliExpress).

## Verified from vendor photos

| | |
|---|---|
| Chip | **IP2326**, marking `IP2326 / 0T41.IDA` — genuine, not a house code |
| Size | **31 × 18 mm** (from the vendor dimension drawing, not estimated) |
| Front pads | `GND`, `VIN+`, `B+`, `B−` |
| Back pads | `LED`, `NTC`, `GND`, and **`BM`** between `B−` and `B+` |
| Config points | `ISET`, `NTC`, `ROV` silkscreened on the front |
| Mechanical | 4 plated corner mounting holes; 2.2 µH inductor (`2R2`); 100 µF 16 V electrolytic |

## What matters

- **`BM` is broken out**, so balancing actually works. Many 2S modules omit it.
- **Charger only, not a BMS.** No `P+`/`P−`, no protection IC, no MOSFET pair — **U1 is still required**, and B+/B− route through U1's P+/P−.
- **Order by the 2S/3S dropdown, not by colour.** The vendor sells both configs in both colours and their photos pair black with 3S.
- **The 3S board (`LX-LSC-V2`) also has a `BM` pad** — but the IP2326 does no balancing in 3S, so it is decoration. Do not be reassured by seeing it.
- **Do not bridge `ROV`** — that is the 3S select.
- **`ISET` must be reworked** down from ~1.5 A. Identify the resistor by the silkscreen and **measure it**; several resistors share the same 3-digit codes. Floor is ~0.5 A at 180 kΩ.
- **Height risk:** the 100 µF electrolytic is the tallest part and stacks on the carrier PCB's 2.6 mm standoff, in a budget with 0.3 mm of slack. **Measure overall height before finalising the enclosure.**

## Files

| File | What it shows |
|---|---|
| `ip2326-purple-2s-z6732-v4.0-front-back.png` | The board to buy. Front and back, `BM` pad visible |
| `ip2326-dimensions-31x18mm.png` | Dimensioned drawing, 31 × 18 mm. Also shows the 3S board alongside |
| `ip2326-black-3s-lx-lsc-v2-front-back.png` | The **3S** board — wrong part, kept so it is recognisable |

## Open

- [ ] Measure overall height including the electrolytic
- [ ] Identify and measure the ISET resistor on a real board
- [ ] Confirm mounting hole positions for the carrier PCB footprint
