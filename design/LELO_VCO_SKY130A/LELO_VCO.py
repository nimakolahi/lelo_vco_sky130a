"""LELO_VCO ciccreator sidecar (cicpy SidecarCell).
First cut: floorplan only (4 device bands as 2 rows). Routing added next.
Instance names come from the xschem netlist: XM0..XM27, x1, x2.
"""
from cicpy.sidecar import SidecarCell, Stack


class LELO_VCO(SidecarCell):

    # ---- NMOS bands ----
    class n_mirror(Stack):          # NMOS current mirror + diode (M26)
        match = r'^XM(1[0-4]|26)$'
        group = "nmos"
        order = ['XM26', 'XM14', 'XM13', 'XM12', 'XM11', 'XM10']

    class n_ring(Stack):            # ring NMOS
        match = r'^XM[0-4]$'
        group = "nmos"
        order = ['XM4', 'XM3', 'XM2', 'XM1', 'XM0']

    class n_buf(Stack):             # output-buffer NMOS
        match = r'^XM2[01]$'
        group = "nmos"
        order = ['XM20', 'XM21']

    class tail(Stack):              # M27 tail (Vin)
        match = r'^XM27$'
        group = "nmos"

    class res(Stack):               # bias resistors
        match = r'^x[12]$'
        group = "res"
        order = ['x1', 'x2']

    # ---- PMOS bands ----
    class p_ring(Stack):            # ring PMOS
        match = r'^XM[5-9]$'
        group = "pmos"
        order = ['XM9', 'XM8', 'XM7', 'XM6', 'XM5']

    class p_mirror(Stack):          # PMOS current mirror + diode (M25)
        match = r'^XM(1[5-9]|24|25)$'
        group = "pmos"
        order = ['XM25', 'XM24', 'XM19', 'XM18', 'XM17', 'XM16', 'XM15']

    class p_buf(Stack):             # output-buffer PMOS
        match = r'^XM2[23]$'
        group = "pmos"
        order = ['XM22', 'XM23']

    # ---- floorplan: bottom row NMOS, top row PMOS ----
    rows = [
        [tail, res, n_mirror, n_ring, n_buf],
        [p_ring, p_mirror, p_buf],
    ]
