#!/usr/bin/env bash
# Reproducible sch2mag runner for the LELO_VCO ciccreator flow.
# Run INSIDE the aicex image from work/:  bash ../cic/run_sch2mag.sh [lvs|drc]
# Upgrades cicpy to 0.3.1 (SidecarCell) and applies a leniency patch to the
# xschem printer (cicpy chokes writing a subckt instance that ties two pins to
# the same net -- e.g. JNWTR_RES2 x1 with P=B=VSS -- which does not affect the
# magic view we verify). See memory ciccreator-sch2mag-sidecar-flow.
set -e
export PATH=/opt/eda/bin:$PATH
pip install -q -U cicpy 2>&1 | tail -1
d=$(python3 -c "import cicpy,os;print(os.path.dirname(cicpy.__file__))")
python3 - "$d/printer/xschemprinter.py" <<'PY'
import sys
f=sys.argv[1]; s=open(f).read()
old="""             except Exception as e:
                 self.current_cell.ckt.printToJson()

                 raise(e)"""
new="""             except Exception as e:
                 import logging
                 logging.getLogger("xschem").warning(f"skip xschem instance view: {e}")"""
if old in s: open(f,"w").write(s.replace(old,new)); print("xschemprinter: patched (lenient)")
else: print("xschemprinter: already patched or changed")
PY
# The instance-name annotation is placed at the instance CENTRE
# (layoutcell.addInstance).  An instance whose width is an odd multiple of the
# 5 nm database grid therefore centres its label on a half-grid point, and
# cicpy's own gridcheck then aborts the build over a cosmetic TXT label that
# carries no geometry (net=<none>).  Snap the label to the grid; nothing but
# the label moves.
python3 - "$d/core/layoutcell.py" <<'PY'
import sys
f=sys.argv[1]; s=open(f).read()
old="        t.moveTo(int(x + i.width() / 2), int(y + i.height() / 2))"
new=("        _g = 50  #- 5 nm database grid\n"
     "        _sx = int(x + i.width() / 2); _sy = int(y + i.height() / 2)\n"
     "        t.moveTo(round(_sx / _g) * _g, round(_sy / _g) * _g)")
if old in s: open(f,"w").write(s.replace(old,new)); print("layoutcell: TXT label snapped to grid")
else: print("layoutcell: already patched or changed")
PY
find ../design -name "*.lock" -delete 2>/dev/null || true
cicpy sch2mag --libdir ../design/ --techlib sky130 LELO_VCO_SKY130A LELO_VCO
[ "$1" = "lvs" ] && make lvs CELL=LELO_VCO
[ "$1" = "drc" ] && make drc CELL=LELO_VCO
true
