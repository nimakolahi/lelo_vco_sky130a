"""LELO_VCO ciccreator sidecar -- per-stage floorplan, REYATR-style open-rail cells.

The leaf cells are now open-rail (guard only on left/right, center clear), so
the maze router can route the internal feeds and crossing nets through the
column centers -- the closed guard ring used to block every lane.

Floorplan (from work/cdl/LELO_VCO.spice): one vertical column per inverter
stage (NMOS mirror-sense M1x below ring Mx; PMOS ring M(5+x) below mirror-leg
M(15+x)), five stages tiled left->right.  Supplies are carried by the abutted
guard rails (declared `blocked`), not routed.
"""
import re
from cicpy.sidecar import SidecarCell, Stack


class _Mirrorable(Stack):
    """Flip the mirror-sense/leg device left-right in afterPlace so its
    drain (the feed node) lands in the same lane as the ring device's
    source -- then the feed routes as one vertical (the rey setAngle
    trick). The mirror devices are the 0p96 (M10-14, M26) / mirror-leg
    (M15-19, M24-25) instances; the ring/buffer devices stay put."""
    mirror_re = None

    def afterPlace(self, entry):
        if self.mirror_re:
            for inst in self.instances:
                nm = getattr(inst, "instanceName", "")
                if re.match(self.mirror_re, nm):
                    x, y = inst.x1, inst.y1
                    inst.setAngle("MY")
                    inst.moveTo(int(x), int(y))
                    inst.updateBoundingRect()
            self.updateBoundingRect()
        return None


class _N(_Mirrorable):
    group = "nmos"
    blocked = [("VSS", "bulk; carried by the abutted guard rails")]


class _P(_Mirrorable):
    group = "pmos"
    blocked = [("VDD_1V8", "bulk; carried by the abutted guard rails")]


class LELO_VCO(SidecarCell):

    channel = 6

    # ---- NMOS stage columns: [mirror-sense (bottom), ring (top)] ----
    class NA0(_N):
        match = r'^(XM10|XM0)$'; order = ['XM10', 'XM0']; mirror_re = r'XM10$'
    class NA1(_N):
        match = r'^(XM11|XM1)$'; order = ['XM11', 'XM1']; mirror_re = r'XM11$'
    class NA2(_N):
        match = r'^(XM12|XM2)$'; order = ['XM12', 'XM2']; mirror_re = r'XM12$'
    class NA3(_N):
        match = r'^(XM13|XM3)$'; order = ['XM13', 'XM3']; mirror_re = r'XM13$'
    class NA4(_N):
        match = r'^(XM14|XM4)$'; order = ['XM14', 'XM4']; mirror_re = r'XM14$'

    # ---- PMOS stage columns: [ring (bottom), mirror-leg (top)] ----
    class PA0(_P):
        match = r'^(XM5|XM15)$'; order = ['XM5', 'XM15']; mirror_re = r'XM15$'
    class PA1(_P):
        match = r'^(XM6|XM16)$'; order = ['XM6', 'XM16']; mirror_re = r'XM16$'
    class PA2(_P):
        match = r'^(XM7|XM17)$'; order = ['XM7', 'XM17']; mirror_re = r'XM17$'
    class PA3(_P):
        match = r'^(XM8|XM18)$'; order = ['XM8', 'XM18']; mirror_re = r'XM18$'
    class PA4(_P):
        match = r'^(XM9|XM19)$'; order = ['XM9', 'XM19']; mirror_re = r'XM19$'

    # ---- references / tail / bias resistors / buffers ----
    class n_diode(_N):
        match = r'^XM26$'
    class p_ref(_P):
        match = r'^(XM25|XM24)$'; order = ['XM25', 'XM24']
    class tail(_N):
        match = r'^XM27$'
    class res(Stack):
        match = r'^x1$'; group = "res"; order = ['x1']
    class n_buf(_N):
        match = r'^XM2[01]$'; order = ['XM21', 'XM20']
    class p_buf(_P):
        match = r'^XM2[23]$'; order = ['XM23', 'XM22']

    # ---- floorplan: bottom row NMOS-well, top row PMOS-well ----
    rows = [
        [res, tail, n_diode, NA0, NA1, NA2, NA3, NA4, n_buf],
        [p_ref, PA0, PA1, PA2, PA3, PA4, p_buf],
    ]

    supplies = [
        {"net": "VDD_1V8", "ring": "t", "strap": "top"},
        {"net": "VSS", "ring": "b", "strap": "bottom"},
    ]

    # ---- crossing nets (drops auto-discovered: every subcell exposing the
    # net, M2, centered) ----
    routes = [
        {"net": "net13", "track": 0},
        {"net": "net10", "track": 1},
        {"net": "net8",  "track": 2},
        {"net": "net6",  "track": 3},
        {"net": "net14", "track": 4},
        {"net": "net17", "track": 5},
        {"net": "net18", "track": 6},
        {"net": "net19", "track": 7},
        {"net": "Vout",  "track": 8},
        {"net": "net16", "track": 9},
    ]
