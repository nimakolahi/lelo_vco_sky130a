# LELO_VCO

Current-starved ring-oscillator VCO in SkyWater 130 nm.

## Interface

| Pin      | Dir   | Description                                  |
|----------|-------|----------------------------------------------|
| VDD_1V8  | in    | Supply (1.8 V nominal)                        |
| VSS      | in    | Ground                                        |
| Vin      | in    | Control voltage — sets the tuning frequency   |
| Vout     | out   | Oscillator output                             |

## Operation

A current-starved ring oscillator. The control voltage `Vin` sets the gate of
the current-starving device (`XM27`), which limits the charge/discharge current
of the ring and therefore the oscillation frequency: higher `Vin` → more
current → higher `f_out`.

## Characterization

- **Transient / corners:** see [../../sim/VCO/README.md](../../sim/VCO/README.md).
- **Tuning curve (f_out vs Vin):** see
  [../../sim/VCO/TUNING.md](../../sim/VCO/TUNING.md) — typical K_VCO ≈ 75 MHz/V,
  usable range ≈ 0.5–1.3 V, ~6 → 67 MHz.

![VCO tuning curve](../../sim/VCO/vco_tuning_curve.png)
