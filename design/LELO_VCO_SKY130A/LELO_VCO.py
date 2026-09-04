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
        if False and self.mirror_re:  # NOTE: overlaps devices; see commit msg
            for inst in self.instances:
                nm = getattr(inst, "instanceName", "")
                if re.match(self.mirror_re, nm):
                    x, y = inst.x1, inst.y1
                    inst.setAngle("MY")
                    inst.moveTo(int(x), int(y))
                    inst.updateBoundingRect()
        return None


class _N(_Mirrorable):
    group = "nmos"


class _P(_Mirrorable):
    group = "pmos"


class LELO_VCO(SidecarCell):

    channel = 24

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
        {"net": "VDD_1V8", "ring": "t", "strap": "top", "pin_strap": True},
        {"net": "VSS", "ring": "b", "strap": "bottom", "pin_strap": True},
    ]

    # ---- crossing nets (drops auto-discovered: every subcell exposing the
    # net, M2, centered) ----
    # Drop SIDES matter: each stage column receives 3 drops (ring-in, ring-out,
    # bias bus). Without sides they share one lane and short (rey_ldo documents
    # this exact failure). Drain-side drop -> "left", gate-side -> "right",
    # bias bus -> "center".
    routes = [
        {"net": "net13", "track": 0, "drops": [[NA0, "M2", "right"], [NA1, "M2", "left"], [PA0, "M2", "right"], [PA1, "M2", "left"]]},
        {"net": "net10", "track": 1, "drops": [[NA1, "M2", "right"], [NA2, "M2", "left"], [PA1, "M2", "right"], [PA2, "M2", "left"]]},
        {"net": "net8",  "track": 2, "drops": [[NA2, "M2", "right"], [NA3, "M2", "left"], [PA2, "M2", "right"], [PA3, "M2", "left"]]},
        {"net": "net6",  "track": 3, "drops": [[NA3, "M2", "right"], [NA4, "M2", "left"], [PA3, "M2", "right"], [PA4, "M2", "left"]]},
        {"net": "net14", "track": 4, "drops": [[NA0, "M2", "left"], [NA4, "M2", "right"], [PA0, "M2", "left"], [PA4, "M2", "right"], [n_buf, "M2", "left"], [p_buf, "M2", "left"]]},
        {"net": "net17", "track": 5, "drops": [[n_diode, "M2", "center"], [NA0, "M2", "center"], [NA1, "M2", "center"], [NA2, "M2", "center"], [NA3, "M2", "center"], [NA4, "M2", "center"], [p_ref, "M2", "left"]]},
        {"net": "net18", "track": 6, "drops": [[p_ref, "M2", "right"], [PA0, "M2", "center"], [PA1, "M2", "center"], [PA2, "M2", "center"], [PA3, "M2", "center"], [PA4, "M2", "center"], [tail, "M2", "left"]]},
        {"net": "net19", "track": 7, "drops": [[n_buf, "M2", "center"], [p_buf, "M2", "center"]]},
        {"net": "Vout",  "track": 8, "drops": [[n_buf, "M2", "right"], [p_buf, "M2", "right"]]},
        {"net": "net16", "track": 9, "drops": [[res, "M2", "center"], [tail, "M2", "right"]]},
        {"net": "VSS", "track": 10, "drops": [[n_diode, "M2"], [NA0, "M2"], [NA1, "M2"], [NA2, "M2"], [NA3, "M2"], [NA4, "M2"], [n_buf, "M2"], [res, "M2"], [tail, "M2"]]},
        {"net": "VDD_1V8", "track": 11, "drops": [[p_ref, "M2"], [PA0, "M2"], [PA1, "M2"], [PA2, "M2"], [PA3, "M2"], [PA4, "M2"], [p_buf, "M2"]]},
        {"net": "VSS", "track": 10, "drops": [[n_diode, "M2"], [NA0, "M2"], [NA1, "M2"], [NA2, "M2"], [NA3, "M2"], [NA4, "M2"], [n_buf, "M2"], [res, "M2"], [tail, "M2"]]},
        {"net": "VDD_1V8", "track": 11, "drops": [[p_ref, "M2"], [PA0, "M2"], [PA1, "M2"], [PA2, "M2"], [PA3, "M2"], [PA4, "M2"], [p_buf, "M2"]]},
    ]
