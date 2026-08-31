# LELO_VCO — ciccreator (generated-layout) environment

Branch `ciccreator`. Goal: rebuild the VCO layout the way the reference LELO
blocks are built — describe it in a `.cic` and generate a clean, DRC/LVS-correct
layout (tapped cells, signals on M2) with ciccreator + cicpy, instead of hand-Magic.
(`master` keeps the hand layout for finishing by hand.)

## Why (see the reference family)
Every analogicus LELO oscillator is GENERATED, not hand-drawn:
  lelo_gr01/oscillator.cic, lelo_gr02/OSCILLATOR.cic, lelo_gr04/LELO_GR04_OSC_v2.cic
They instantiate the **jnw_atr** tapped cells (JNWATR_NCH/PCH_*) and route on M2.
The hand LELO_VCO used stripped cicpy gencells on M1 -> the fused mesh we fought.

## The flow (from tech/make/core.make `ip:` target)
    make ip     # 1) cic  ../cic/ip.json ../cic/sky130.tech LELO_VCO   -> LELO_VCO.cic
                # 2) cicpy transpile LELO_VCO.cic ../cic/sky130.tech LELO_VCO --magic ... -> .mag
    make view   # cicpy gui LELO_VCO.cic   (interactive place/route tweak)

## Tools
- ciccreator: cloned at `aicex/ciccreator` (C++/Qt). NEEDS BUILDING — no local qmake.
  Build inside the aicex docker image (has Qt), or just rely on the image's prebuilt `cic`:
      docker run --rm -v <aicex>:/home/aicex -w /home/aicex/ciccreator \
        wulffern/aicex:26.04_latest bash -lc 'qmake && make -j4'   # -> bin/cic
  (If `aicex/ciccreator/bin/cic` is absent, core.make falls back to `cic` on PATH = the image's build.)
- cicpy: in the aicex docker image (drives transpile + GUI).

## What's set up here (cic/)
- sky130.tech          — ciccreator tech (copied from jnw_atr)
- hand_placements.txt  — your 30 hand placements (rows) — the SEED for the .cic
- devices.txt          — the 8 device types (W/L) to map onto jnw_atr JNWATR_* cells

## Design steps (to do)
1. Build/verify `cic` and `cicpy` (docker, above).
2. Map each LELO device (devices.txt) to a JNWATR_* tapped-cell variant
   (by fingers/contacts) — see jnw_atr transistors.json / gr04 OSC .cic for examples.
3. Author `cic/ip.json` (top cell LELO_VCO): place the transistors in the 4 rows
   from hand_placements.txt, add JNWATR TAPTOP/TAPBOT tap cells per band.
4. Add the ROUTING on M2 per the LVS net checklist (net17->M26 diode, net18->M25 diode,
   ring hops, Vout, Vin) — same target list already verified against the schematic.
5. `make ip` -> `make drc lvs`. Iterate in `make view` (cicpy gui).

## Reference templates
- jnw_atr: cic/ip.py, ip.json, transistors.json (how tapped cells are declared)
- lelo_gr01 design/oscillator.cic (closest: ring oscillator) — study its M2 routing

## ✅ Environment is BUILT and WORKING (arm64)
- `aicex/ciccreator/bin/linux/cic` — compiled natively on arm64 (Qt6). Verified: compiles a .cic.
- Docker image **`lelo-cic:latest`** — ubuntu22.04 + Qt6 runtime + cicpy. Runs BOTH `cic` and `cicpy transpile`.
  (aicex image has no Qt6, so run the `cic`/transpile steps in `lelo-cic`; DRC/LVS in the aicex image.)

### Run the flow (once cic/ip.json exists)
    # cic + transpile  ->  design/LELO_VCO_SKY130A/LELO_VCO.mag
    docker run --rm -v <aicex>:/home/aicex -w /home/aicex/ip/lelo_vco_sky130a/design \
      lelo-cic:latest bash -lc '\
        ../../ciccreator/bin/linux/cic --I ../cic ../cic/ip.json ../cic/sky130.tech LELO_VCO && \
        cicpy transpile LELO_VCO.cic ../cic/sky130.tech LELO_VCO --magic --spice'
    # then DRC/LVS in the aicex image as usual:  make drc lvs CELL=LELO_VCO

## ⭐ Recommended path: AI-assisted `sch2mag` sidecar (from wulffern/rey_ldo_sky130a)
That LDO repo is the **proven AI-assisted flow** (Claude Code did the layout). Cleaner than
hand-authoring `ip.json` — it's declarative and you iterate at the *specification* level.

**How it works**
- `cicpy sch2mag` reads the **schematic** + a Python **sidecar** (`<CELL>.py`, a `SidecarCell`
  subclass) + **`.groups.yaml`**, and emits a *placed + routed* layout.
- Placement: `rows = [[...],[...]]` + a class per logical group (`match` regex on instances,
  explicit `order`, `group` -> .groups.yaml). Mirroring via `afterPlace()`.
- Routing: `paths`/`routes` — ChannelRoute with `track` + `drops` per net/layer (M2).
- Physical props (tap/well/width/stacking) come from `.groups.yaml`, decoupled from the .py.
- Hooks: `beforePlace / afterPlace / beforeRoute / afterPorts`.
- Loop: **build -> check DRC/LVS -> change ONE declared thing.**

**Maps directly onto LELO_VCO**
    rows = [[ NMOS current mirror: M26 M10..M14 ],
            [ ring NMOS + buffer: M0..M4 M20 M21 ],
            [ ring PMOS + buffer: M5..M9 M22 M23 ],
            [ PMOS current mirror: M25 M24 M15..M19 ]]   # = hand_placements.txt rows
    groups: nmos (p-sub tap), pmos (nwell tap)           # taps for free
    routes: net17->M26 diode, net18->M25 diode, ring hops, Vout, Vin  # M2, per net checklist

**To do (needs Docker up)**
1. Verify image cicpy supports `SidecarCell` (rey_ldo is recent — may need `pip install -U cicpy`).
2. Draft `design/LELO_VCO_SKY130A/LELO_VCO.py` (sidecar) + `.groups.yaml` from the rey_ldo template.
3. `cicpy sch2mag` -> layout -> `make drc lvs` -> iterate one declaration at a time.

**vs the `ip.json` path (already in this branch):** `ip.json` compiles end-to-end today but is
lower-level and needs device sizing. The `sch2mag` sidecar is the higher-level, proven route —
prefer it for the clean, LVS-matching result.
