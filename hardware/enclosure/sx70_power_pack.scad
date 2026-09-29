// SX-70 External Power Pack — parametric enclosure
// 2S LiPo (Gens Ace 350mAh) + 2S protection board + IP2326 USB-C charger
// + Pololu 6V buck + Schottky + series R, output on 2 pogo pins to the
// camera's base-plate contacts. Most parts live on the carrier PCB — see
// docs/pcb.md; this file is the shell only.
//
// Units: mm. Print base + lid in PETG (sustained load, possible heat in a bag).
// Set `part` to "base", "lid", or "both" (preview layout).
//
// All component envelopes are generous placeholders — measure your actual
// parts with calipers and update the /* [Bays] */ and /* [Cutouts] */ values.

/* [Render] */
part = "both";            // [base, lid, both]
// Which power architecture this shell is for:
//   "lipo" = 2S LiPo + charger + buck regulator
//   "aaa4" = 4x XTAR 1.5V regulated AAA in series, no converter
battery_option = "lipo";  // [lipo, aaa4]
$fn  = 48;

/* [Shell] */
wall       = 2.0;
floor_t    = 1.6;         // mounting face thickness
lid_t      = 1.6;
// Clear height needed ABOVE the magnet backing pads (LiPo 10 + BMS ~2.5;
// AAA holder ~12). The cavity is deepened automatically to keep this clear.
inner_h    = (battery_option == "aaa4") ? 14.0 : 13.0;
corner_r   = 3.0;
clearance  = 0.2;         // lid lip fit

/* [Bays] */
// aaa4: 4-cell AAA holder (~46 x 46 x 12); electronics bay holds only the cap,
//       series resistor and switch.
// lipo sizing follows the L-shaped carrier PCB in docs/pcb.md: the battery sits
// on the case floor beside the board, and the board's tongue reaches the far
// pogo pin. The divider is removed for lipo because the tongue crosses it.
batt_bay_l = (battery_option == "aaa4") ? 48.0 : 36.0;
elec_bay_l = (battery_option == "aaa4") ? 24.0 : 46.0;
inner_w    = (battery_option == "aaa4") ? 48.0 : 46.0;
divider    = (battery_option == "aaa4");
divider_t  = 1.2;

// Hard ceiling: the camera bottom is 95 mm wide, so outer_l must stay under it.
camera_max_w = 95.0;
divider_h  = 9.0;         // lower than inner_h so leads pass over it

/* [Lid screws] */
// Brass heat-set inserts in the base, machine screws through the lid.
// Defaults are for M2.5 short inserts (3.5 mm OD x 4.0 mm long) — the usual
// small-insert size. Measure YOUR inserts: OD and length vary by supplier.
insert_d      = 3.4;      // bore: insert OD minus ~0.1 for the melt interference
insert_l      = 4.0;      // insert length
insert_relief = 0.5;      // extra bore depth below the insert
insert_lead   = 0.5;      // chamfer at the boss mouth, to start the insert square
// Boss OD needs ~1.5 mm of PETG around the bore or the insert splits it out.
boss_d        = insert_d + 3.0;
lid_screw_d   = 2.7;      // M2.5 clearance
lid_csk_d     = 5.0;      // M2.5 countersunk head
lip_h         = 1.2;
lip_w         = 1.0;

/* [Magnets] */
// Discs bonded into pockets on the outer (camera-facing) face, mating to a
// steel shim on the camera. Bonded, not press-fit: the pocket is deliberately
// loose to leave room for epoxy.
magnets       = true;
magnet_d      = 6.0;
magnet_t      = 2.0;
magnet_fit    = 0.15;     // per-side clearance for adhesive
magnet_recess = 0.3;      // sits below the face so it can't scratch the camera
magnet_back   = 0.8;      // minimum PETG left behind the magnet
magnet_wall   = 2.0;      // PETG around the pocket
// Leave empty for four auto-placed pockets; otherwise list [x, y] outer coords.
magnet_pos    = [];

/* [Pogo pins] */
// Camera interface: spring-loaded pins through the camera-facing face, pressing
// into the base-plate contacts through 3 mm holes in the skin.
//
// Specified pin: Mill-Max 7982-1-15-20-75-14-11-0 (through-hole) — 2.1 mm body,
// 0.7 mm stroke, 60 g mid-stroke, 8 A, gold throughout. Held by the CARRIER PCB.
//
// !! pogo_spacing IS A PLACEHOLDER (50 mm). Measure it on your own base plate.
//
// With only 0.7 mm of stroke, PROTRUSION IS A MEASURED DIMENSION. Tune it with
// pcb_standoff. The echo at the bottom reports the result and warns if it drops
// below the stroke.
//
// The 50 mm span is wider than either bay, so the pins sit in a lane along one
// edge, placed against the whole shell rather than a bay.
pogo_pins    = true;
// The pins are now held by the CARRIER PCB, not by the plastic. The shell only
// needs a clearance bore for each plunger, so pogo_boss is off by default.
pogo_boss    = false;     // true = old press-into-plastic build
pogo_body_d  = 2.1;       // pin barrel (7982 = 2.1 mm)
pogo_clear   = 0.4;       // extra bore clearance when the PCB holds the pin
pogo_above   = 5.2;       // pin height above its mounting surface, from datasheet
pogo_stroke  = 0.7;       // datasheet stroke
pcb_standoff = 2.6;       // PCB underside above the inner floor — sets protrusion
pogo_spacing = 50.0;      // centre-to-centre — PROVISIONAL, confirm on a camera
pogo_lane    = 8.0;       // pin centreline, in from the inner wall
pogo_lead    = 0.4;       // outer lead-in chamfer
pogo_pad_h   = 2.5;       // extra grip length inside, for the press fit
pogo_wall    = 2.5;       // PETG around the bore
// Explicit, not auto-centred: the PCB layout needs the left end of the lane
// clear for J3 and a mounting hole, which pushed both pins 3 mm right.
pogo_pos     = [[21, 10], [71, 10]];   // outer coords; [] = auto-centre

/* [Cutouts] */
// USB-C receptacle on the electronics end wall
usb_w      = 9.6;
usb_h      = 3.8;
usb_y      = 9.0;         // centre, measured from inner wall (y=0 side)
usb_z      = 3.4;         // centre above floor: foam tape + PCB + half receptacle
// Output cable exit — not needed since J1 was dropped. The only things crossing
// the shell wall are the USB-C port, the switch actuator and the pogo plungers.
// Set cable_exit = true to restore it for a wired bench output.
cable_exit = false;
cable_d    = 3.6;
cable_y    = 28.0;
cable_z    = 5.0;
// Slide switch (SS12D00-style) actuator slot on the y=0 long wall
sw_slot_l  = 7.5;
sw_slot_h  = 3.4;
sw_x       = 20.0;        // centre, from the start of the electronics area
sw_z       = 6.0;
// Charge LED window in lid (over the IP2326 LEDs)
led_d      = 2.5;
led_x      = 30.0;        // from the start of the electronics area
led_y      = 8.0;         // from inner y=0 wall

/* [Mounting face] */
// The folding SX-70 has no tripod socket. Default is a flat face for VHB.
// If you screw it to the camera base, list hole centres in outer
// coordinates [x, y] after measuring your body.
mount_holes    = [];      // e.g. [[10,19],[77,19]]
mount_hole_d   = 2.2;
mount_cbore_d  = 4.2;     // head recess from inside
mount_cbore_h  = 0.8;

// ---------- derived ----------
inner_l = batt_bay_l + (divider ? divider_t : 0) + elec_bay_l;
outer_l = inner_l + 2*wall;
outer_w = inner_w + 2*wall;
div_x   = wall + batt_bay_l;              // divider start (outer coords)
elec_x0 = div_x + (divider ? divider_t : 0);   // electronics bay start

mag_pocket_d = magnet_d + 2*magnet_fit;
mag_pocket_h = magnet_t + magnet_recess;
// Pocket is deeper than the floor, so raise a local pad inside to back it.
mag_pad_h    = max(0, mag_pocket_h + magnet_back - floor_t);
mag_pad_d    = mag_pocket_d + 2*magnet_wall;
mag_inset    = mag_pad_d/2 + 1.0;

pogo_pad_d  = pogo_body_d + 2*pogo_wall;
pogo_bore_d = pogo_boss ? pogo_body_d : pogo_body_d + 2*pogo_clear;
// Boss build: bore depth sets protrusion. PCB build: standoff sets it.
pogo_grip  = pogo_boss ? floor_t + pogo_pad_h : floor_t + pcb_standoff;
pogo_stick = pogo_above - pogo_grip;
// 50 mm spacing exceeds either bay, so the pins are placed against the WHOLE
// shell and sit in a clear lane along one edge — see docs/pcb.md.
pogo_cx    = outer_l/2;
pogo_pts = len(pogo_pos) == 0
  ? [ [pogo_cx - pogo_spacing/2, wall + pogo_lane],
      [pogo_cx + pogo_spacing/2, wall + pogo_lane] ]
  : pogo_pos;

// Cavity is deepened by the tallest internal pad so `inner_h` stays clear.
pad_max = max(magnets ? mag_pad_h : 0, (pogo_pins && pogo_boss) ? pogo_pad_h : 0);
cav_h   = inner_h + pad_max;
base_h  = floor_t + cav_h;
mag_pts = len(magnet_pos) == 0
  ? [ [outer_l*0.25, wall + mag_inset], [outer_l*0.75, wall + mag_inset],
      [outer_l*0.25, outer_w - wall - mag_inset],
      [outer_l*0.75, outer_w - wall - mag_inset] ]
  : magnet_pos;

bo = boss_d/2 - 0.6;                       // bosses overlap the walls slightly
boss_pos = [
  [wall + bo,           wall + bo],
  [outer_l - wall - bo, wall + bo],
  [wall + bo,           outer_w - wall - bo],
  [outer_l - wall - bo, outer_w - wall - bo]
];

module rbox(size, r) {
  hull()
    for (x = [r, size[0] - r], y = [r, size[1] - r])
      translate([x, y, 0]) cylinder(r = r, h = size[2]);
}

module slot_y(w, h, depth) {
  // rounded slot, long axis along y, cut through an x-facing wall
  r = h/2;
  hull()
    for (dy = [-(w/2 - r), (w/2 - r)])
      translate([0, dy, 0]) rotate([0, 90, 0]) cylinder(r = r, h = depth, center = true);
}

module base() {
  difference() {
    union() {
      difference() {
        rbox([outer_l, outer_w, base_h], corner_r);
        translate([wall, wall, floor_t]) cube([inner_l, inner_w, cav_h + 1]);
      }
      // divider between battery and electronics (omitted when the PCB crosses it)
      if (divider)
        translate([div_x, wall - 0.5, floor_t - 0.1]) cube([divider_t, inner_w + 1, divider_h + 0.1]);
      // lid screw bosses
      for (p = boss_pos)
        translate([p[0], p[1], floor_t - 0.1]) cylinder(d = boss_d, h = cav_h + 0.1);
      // magnet backing pads (the pocket is deeper than the floor)
      if (magnets && mag_pad_h > 0)
        for (m = mag_pts)
          translate([m[0], m[1], floor_t - 0.01])
            cylinder(d = mag_pad_d, h = mag_pad_h + 0.01);
      // pogo pin bosses — only for the legacy press-into-plastic build
      if (pogo_pins && pogo_boss)
        for (g = pogo_pts)
          translate([g[0], g[1], floor_t - 0.01])
            cylinder(d = pogo_pad_d, h = pogo_pad_h + 0.01);
    }
    // heat-set insert bores, open at the boss top, with a lead-in chamfer
    for (p = boss_pos) {
      translate([p[0], p[1], base_h - (insert_l + insert_relief)])
        cylinder(d = insert_d, h = insert_l + insert_relief + 1);
      translate([p[0], p[1], base_h - insert_lead])
        cylinder(d1 = insert_d, d2 = insert_d + 2*insert_lead, h = insert_lead + 0.01);
    }

    // magnet pockets, open on the outer/camera face
    if (magnets)
      for (m = mag_pts)
        translate([m[0], m[1], -0.01]) cylinder(d = mag_pocket_d, h = mag_pocket_h + 0.01);

    // pogo pin bores, through the camera-facing face, with an outer lead-in
    if (pogo_pins)
      for (g = pogo_pts) {
        translate([g[0], g[1], -1])
          cylinder(d = pogo_bore_d, h = floor_t + (pogo_boss ? pogo_pad_h : 0) + 2);
        translate([g[0], g[1], -0.01])
          cylinder(d1 = pogo_bore_d + 2*pogo_lead, d2 = pogo_bore_d, h = pogo_lead + 0.01);
      }

    // USB-C on the electronics end wall
    translate([outer_l - wall/2, wall + usb_y, floor_t + usb_z])
      slot_y(usb_w, usb_h, wall + 2);
    // output cable exit (optional — see cable_exit)
    if (cable_exit)
      translate([outer_l - wall/2, wall + cable_y, floor_t + cable_z])
        rotate([0, 90, 0]) cylinder(d = cable_d, h = wall + 2, center = true);
    // switch actuator slot on y=0 wall
    translate([elec_x0 + sw_x - sw_slot_l/2, -1, floor_t + sw_z - sw_slot_h/2])
      cube([sw_slot_l, wall + 2, sw_slot_h]);

    // optional screw mounting through the floor
    for (h = mount_holes) {
      translate([h[0], h[1], -1]) cylinder(d = mount_hole_d, h = floor_t + 2);
      translate([h[0], h[1], floor_t - mount_cbore_h]) cylinder(d = mount_cbore_d, h = 2);
    }
  }
}

module lid() {
  difference() {
    union() {
      rbox([outer_l, outer_w, lid_t], corner_r);
      // locating lip that drops inside the walls, notched around bosses
      difference() {
        translate([wall + clearance, wall + clearance, lid_t])
          cube([inner_l - 2*clearance, inner_w - 2*clearance, lip_h]);
        translate([wall + clearance + lip_w, wall + clearance + lip_w, lid_t - 0.1])
          cube([inner_l - 2*clearance - 2*lip_w, inner_w - 2*clearance - 2*lip_w, lip_h + 1]);
        for (p = boss_pos)
          translate([p[0], p[1], lid_t - 0.1]) cylinder(d = boss_d + 1, h = lip_h + 1);
      }
    }
    // countersunk lid screws (lid is modelled face-down; csk on the outer face z=0)
    for (p = boss_pos) {
      translate([p[0], p[1], -1]) cylinder(d = lid_screw_d, h = lid_t + lip_h + 2);
      translate([p[0], p[1], -0.01]) cylinder(d1 = lid_csk_d, d2 = lid_screw_d, h = (lid_csk_d - lid_screw_d)/2);
    }
    // LED window. Lid is printed face-down and flipped about its long (x) axis
    // to install, so y is mirrored here.
    translate([elec_x0 + led_x, outer_w - (wall + led_y), -1])
      cylinder(d = led_d, h = lid_t + lip_h + 2);
  }
}

if (part == "base") base();
else if (part == "lid") lid();
else {
  base();
  translate([0, outer_w + 8, 0]) lid();
}

echo(str("Outer envelope: ", outer_l, " x ", outer_w, " x ", base_h + lid_t, " mm"));
if (outer_l > camera_max_w)
  echo(str("ERROR: outer_l ", outer_l, " mm exceeds the ", camera_max_w,
           " mm camera bottom width"));
else
  echo(str("  long axis fits the ", camera_max_w, " mm camera bottom with ",
           camera_max_w - outer_l, " mm to spare"));
echo(str("Clear height above magnet pads: ", inner_h, " mm"));
echo(str("Lid fixing: ", len(boss_pos), " x M2.5 heat-set inserts, bore ", insert_d,
         " mm x ", insert_l + insert_relief, " mm deep"));
if (pogo_pins) {
  echo(str("Pogo pins: 2 x bore ", pogo_body_d, " mm at ", pogo_spacing,
           " mm spacing — SPACING IS A PLACEHOLDER, MEASURE IT"));
  echo(str("  held by ", pogo_boss ? "printed boss" : "carrier PCB",
           "; effective depth ", pogo_grip, " mm, plunger protrudes ", pogo_stick,
           " mm, stroke ", pogo_stroke, " mm"));
  if (pogo_stick < pogo_stroke)
    echo(str("  WARNING: protrusion ", pogo_stick, " mm is less than the ",
             pogo_stroke, " mm stroke — the pin cannot fully compress. Reduce ",
             pogo_boss ? "pogo_pad_h." : "pcb_standoff."));
  if (pogo_stick <= 0)
    echo(str("  ERROR: pin does not reach past the outer face. Reduce ",
             pogo_boss ? "pogo_pad_h." : "pcb_standoff."));
}
if (magnets)
  echo(str("Magnets: ", len(mag_pts), " x ", magnet_d, " x ", magnet_t,
           " mm discs, pocket ", mag_pocket_d, " mm x ", mag_pocket_h,
           " mm, backing pad ", mag_pad_h, " mm"));
