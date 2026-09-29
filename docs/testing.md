# Bench testing

Two measurements decide the architecture. Do them before ordering anything expensive.

## 0. Are the base-plate contacts a real power rail?

**Do this first.** The whole pogo-pin approach rests on it, and it is currently an assumption. The community describes these as "test points," which is not the same as the main power rail.

1. Fresh film pack loaded. Meter across the two base-plate contacts — expect ~6 V. **Record which is positive.**
2. Watch the voltage at the contacts while firing the shutter. A real rail sags slightly under ~1 A. A high-impedance test tap **collapses**.
3. Measure contact spacing and hole positions on your own body. Model variation across SX-70 Model 1/2/3, Alpha and SE is likely.

If step 2 collapses, pogo pins onto these contacts will not run the camera and the connection has to move.

## 1. Camera floor voltage

**Question:** how low can the supply go before the camera misbehaves? This sets the regulation target and says whether a fixed 6 V module minus a diode drop is acceptable.

1. Camera on the bench supply via a dummy pack, empty film pack loaded, current limit ~3 A.
2. Start at 6.2 V. Cycle the motor. Note behaviour.
3. Step down in 0.1 V increments, cycling at each step.
4. Record three thresholds: where ejection first sounds sluggish, where the solenoid or electronics misbehave, and where it stalls outright.

Record the numbers here and in the master repair notes — they're useful well beyond this project.

| Voltage | Motor | Solenoid / electronics | Notes |
|---|---|---|---|
| 6.2 V | | | |
| 6.0 V | | | |
| 5.8 V | | | |
| 5.6 V | | | |
| 5.4 V | | | |
| 5.2 V | | | |
| 5.0 V | | | |

## 2. Motor current profile

**Question:** what is the actual peak? Anything above 2 A rules out Option A, because the XTAR cells cap there.

1. 0.1 Ω shunt in the supply's return leg, scope across it (100 mV/A).
2. Capture a full eject-and-recock cycle at 6.0 V.
3. Log: inrush peak and its duration, sustained running current, and stalled-rotor current (jam the mechanism briefly, with the supply current-limited).
4. Repeat with the film door open and closed if behaviour differs.

| Measurement | Value | Notes |
|---|---|---|
| Inrush peak | | Duration: |
| Sustained | | |
| Stalled rotor | | |
| Cycle duration | | |

**Decision rule:** peak below ~1.8 A → build Option A. Above 2 A → build Option B. In between, either works; Option B has margin, Option A has fewer failure modes.

Use the sustained figure and cycle duration to sanity-check the energy-per-cycle estimate in [design.md](design.md), and the stalled figure to choose R1.

## 3. Pack bring-up (before it touches a camera)

Option B:

1. Charger alone on the cells, no load: charge current ≤ 1C, termination at 8.4 V, cell midpoint balanced within ~20 mV. Let the CV taper run to termination before measuring the midpoint — balancing only happens in that final phase, so an early reading tells you nothing. Re-check the midpoint every few months; see [design.md](design.md#balancing) for the drift thresholds.
2. Protection board: confirm it cuts on a deliberate short through a fused lead.
3. Regulator into a resistive dummy load: set output so the camera will see the target voltage under load; confirm the low-voltage cutoff trips near 6.4 V.
4. Switch off: confirm standby current is in the µA range.

Option A:

1. Charge all four cells; confirm they're within ~20 mV of each other off the charger.
2. String voltage 6.0 V under no load, and under a 1 A and 2 A resistive load — watch for fold-back or hiccup.

## 4. In-camera

1. Empty film pack, pack connected, several motor cycles.
2. Scope the rail at the JST during ejection. Look for sag below the floor voltage from test 1, and for any hiccup pattern from regulated cells.
3. Tune R1 from the data: enough impedance to limit a jam, not enough to drag the rail under the floor.
4. Only then load film. Shoot a known scene and compare exposure against a PolaPulse-powered frame, especially if magnets are used for mounting.
