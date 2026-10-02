# SX-70 External Power Pack

A rechargeable, camera-mounted power supply for the folding Polaroid SX-70, replacing the PolaPulse cell in the film pack. Aimed at battery-less film (i-Type), dead packs, and bench work.

**Status: design v0.4, not yet built.** Nothing has been measured on a camera yet. See [Where things stand](#where-things-stand).

## Where things stand

**Settled**

| | |
|---|---|
| Camera interface | Two **pogo pins** onto the base-plate contacts, through 3 mm holes in the skin. **No soldering to the camera** |
| Mounting | Magnets bonded into the pack base, against a VHB-bonded steel shim on the camera |
| Enclosure | 3D printed PETG, M2.5 brass heat-set inserts, magnet pockets and pogo bosses in the base |
| Architecture | Still two options. The measured motor peak current decides between them |
| Envelope (Option B) | **86 × 50 × 17.7 mm** |

**Ordered** — replacement flex parts, in case a flex fails (see [flex-order.md](docs/flex-order.md))

- **Body flex** — Cundari's replacement, ordered from PCBWay, shipped Sept 2026
- **Motor control chips** — 10 assembled boards from PCBWay, ~$135 the lot, Sept 2026, 18–20 day quoted build

Order numbers, the cost breakdown and vendor correspondence are kept out of the repo in a gitignored `private/` folder.

**Not yet ordered** — [digikey-order.csv](hardware/bom/digikey-order.csv) is the consolidated list. Pogo pins, the 0.1 Ω shunt and the R1 spread are the ones that unblock bench work. The LiPo, IP2326, Pololu regulator, magnets and inserts come from other suppliers.

**Blocked on bench measurement** — all three in [testing.md](docs/testing.md), and everything downstream waits on them.

## The problem

The SX-70 draws all its power from the film pack's battery. i-Type and Go film packs have no battery, and old SX-70 packs are frequently dead, so the camera appears completely inert. A PolaPulse supplies about 6 V with roughly 0.5 Ω of internal resistance, and that impedance is an accidental but useful current limiter during a jam. Any replacement needs to supply ~6 V *and* not be a stiff, low-impedance source.

## Two architectures

Both feed the camera through **two pogo pins onto the base-plate contacts** — no soldering to the camera. See [Camera connection](docs/design.md#camera-connection).

### Option A — 4× regulated 1.5 V AAA (no converter)

Four XTAR 1.5 V Li-ion AAA cells in series give a flat 6.0 V with no buck converter, no charge circuit, and nothing to tune. Simplest possible build; matches the Retrospekt approach.

- **Gating spec:** each cell is rated 2 A max, so the string is capped at 2 A.
- Charging happens off-camera in an XTAR charger.
- Energy: ~6.5 Wh.

### Option B — 2S LiPo + USB-C charger + adjustable buck

A small 2S LiPo, an IP2326 USB-C boost charger with cell balancing, and a Pololu fine-adjust regulator with an adjustable low-voltage cutoff.

- Charges in place over USB-C; output dialled to whatever the camera actually needs.
- Ample peak current (30C on a 350 mAh pack is >10 A).
- Energy: ~2.6 Wh, still several hundred exposures per charge.
- Balancing is passive and only runs at the end of the charge, so let the taper finish instead of unplugging at "nearly full" — the protection board will not correct drift on its own ([details](docs/design.md#balancing)).

```
Option A:  4x AAA (6.0 V) --> SW --> C1 --> R1 --> pogo pins --> camera base-plate

Option B:  USB-C --> IP2326 --> 2S protection --> 2S LiPo
                       |                            |
                     (BM balance)                   v
                            SW (EN) --> D30V33MALCMA --> C1 --> D1 --> R1 --> pogo pins --> camera
```

C1 (1000 µF low-ESR) and R1 (0.22–0.47 Ω) appear in both: the capacitor for motor inrush, the resistor to emulate PolaPulse source impedance. D1 (SS34 Schottky) blocks backfeed when a battery-equipped film pack is loaded. **The pogo pins' own contact resistance (40 mΩ for the pair) counts against R1's budget** — measure and subtract.

## Repository layout

```
docs/design.md        Full design notes, calculations, rationale
docs/testing.md       Bench procedure and the measurements that settle open questions
docs/flex-order.md    Replacement body/lens flex: routes and PCBWay order prep
docs/pcb.md           Carrier PCB: constraints, outline, placement, nets, fab spec
hardware/enclosure/   Parametric OpenSCAD enclosure
hardware/bom/         Bills of materials, plus per-part reference material in <ref>-<part>/
hardware/flex-lens/   Lens/shutter flex reverse-engineering: scan spec, KiCad setup, fab drawing
scripts/build_stl.py  Render every STL variant
```

## Building the enclosure

The shell is parametric for both options:

```bash
python scripts/build_stl.py          # renders lipo_{base,lid}.stl and aaa4_{base,lid}.stl
```

Or open `hardware/enclosure/sx70_power_pack.scad` in OpenSCAD and use the Customizer. Set `battery_option` to `lipo` or `aaa4`.

Print in **PETG** (sustained load, possible heat), base floor-down. All component envelopes are placeholders — caliper the real parts and update the parameters before printing a final shell.

The lid closes on **four M2.5 brass heat-set inserts** with countersunk machine screws, and the pack is held to the camera by **four 6 × 2 mm magnets epoxied into pockets in the base**, mating to a steel shim on the camera. Install inserts before bonding magnets — both involve heat. Two **spring-loaded pogo pins** pass through the camera-facing face into the base-plate contacts. Both the magnet pockets and the pogo bores need internal bosses, and those bosses set the shell height; see [Mechanical](docs/design.md#mechanical).

## Open questions

- [ ] **Are the base-plate contacts a real power rail?** The whole pogo-pin approach rests on this and it is unverified — the community calls them "test points". Watch the voltage there while firing: a rail sags under load, a test tap collapses. [testing.md step 0](docs/testing.md)
- [ ] **Camera floor voltage.** Walk a bench supply down in 0.1 V steps and find where cycling degrades. Sets the regulation target.
- [ ] **Motor peak current.** Measure inrush, sustained and stalled-rotor current with a 0.1 Ω shunt. If the peak is below ~1.8 A, Option A wins on simplicity. Above 2 A, Option B.
- [ ] **Contact spacing and pin diameter.** `pogo_spacing` and `pogo_body_d` in the SCAD are placeholders. Measure your own base plate and the pins you buy.
- [ ] **Does Option A need D1 too?** Option B has the Schottky; Option A's BOM does not. Both now connect to the same rail as the film-pack battery, so the backfeed case looks identical. Decide deliberately rather than by omission.
- [ ] **Option A shell is too small.** The 46 mm AAA holder fouls the corner lid bosses in a 48 mm cavity. Needs widening if Option A survives the current measurement.
- [ ] **Force-charging a film-pack battery.** D1 blocks film → pack but not pack → film. Decide between the procedural mitigation and a sense-and-latch inhibit.
- [ ] **Mounting location.** Magnets-in-pack against a VHB-bonded steel shim is settled; *where* on the camera base is not. Must clear the film door and keep magnets away from the motor and shutter solenoid. Re-shoot a test frame after mounting.
- [ ] **Magnets vs pogo spring force.** Two pins push back 100–300 g. Test holding force with pins fitted and compressed.

## Safety notes

- **Switch the pack off before loading film that has its own battery** (SX-70/600). With the pack on, a depleted film battery is force-charged at up to 2 A — and a PolaPulse is a non-rechargeable zinc-chloride cell that can vent. Switched off, the pack is genuinely isolated. See [Film with its own battery](docs/design.md#film-with-its-own-battery--partial-protection-and-a-real-gap).
- Do not solder directly to lithium cells.
- Option B uses raw LiPo cells: the protection board is not optional.
- Verify contact polarity against a real film pack's battery with a meter before connecting anything.
- The pogo pins are exposed on the outside of the pack. Switch it off in a bag, and keep the reverse-polarity protection.

## License

MIT (see `LICENSE`). Consider CERN-OHL-S or -P instead if the hardware matters more than the scripts.
