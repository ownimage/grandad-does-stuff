import pyclipper
from dataclasses import dataclass
from typing import List

from .pen_nib import PenNib
from .vector import Vector

import pyclipper
from dataclasses import dataclass
from typing import List

SCALE = 1000.0

def v_to_int(p: Vector):
    return (int(round(p.x * SCALE)), int(round(p.y * SCALE)))

def int_to_v(p):
    return Vector(p[0] / SCALE, p[1] / SCALE)

@dataclass(frozen=True)
class CompoundPenOutlineRingClipper:
    nib: PenNib
    points: List[Vector]
    inset: float  # border thickness

    def svg_paths(self) -> str:
        if len(self.points) < 2:
            return ""

        # ---------------------------------------------------------
        # 1. Build the nib polygon (4 points) in integer coords
        # ---------------------------------------------------------
        nib_poly = [
            v_to_int(self.nib.tl),
            v_to_int(self.nib.tr),
            v_to_int(self.nib.br),
            v_to_int(self.nib.bl)
        ]

        # ---------------------------------------------------------
        # 2. Build the centre-line polyline
        # ---------------------------------------------------------
        center_path = [v_to_int(p) for p in self.points]

        # ---------------------------------------------------------
        # 3. Minkowski sum: centre-line ⊕ nib
        #    This gives the TRUE broad-nib stroke outline
        # ---------------------------------------------------------
        stroke_polys = pyclipper.MinkowskiSum(nib_poly, center_path, True)

        # Union all resulting polygons
        pc = pyclipper.Pyclipper()
        pc.AddPaths(stroke_polys, pyclipper.PT_SUBJECT, True)
        union = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)

        if not union:
            return ""

        # Take the largest polygon as the outer outline
        outer = max(union, key=pyclipper.Area)

        # ---------------------------------------------------------
        # 4. Inset the outer outline to create the hollow centre
        # ---------------------------------------------------------
        insetter = pyclipper.PyclipperOffset()
        insetter.AddPath(outer, pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)

        inner_solutions = insetter.Execute(-self.inset * SCALE)
        inner = inner_solutions[0] if inner_solutions else []

        # ---------------------------------------------------------
        # 5. Convert to SVG
        # ---------------------------------------------------------
        def path_from_int(path):
            pts = [int_to_v(p) for p in path]
            d = f"M {pts[0].x} {pts[0].y} " + " ".join(
                f"L {p.x} {p.y}" for p in pts[1:]
            ) + " Z"
            return d

        outer_d = path_from_int(outer)

        svg = f'<path d="{outer_d}" fill="black" stroke="none" />\n'

        if inner:
            inner_d = path_from_int(inner)
            svg += f'<path d="{inner_d}" fill="white" stroke="none" />\n'

        return svg