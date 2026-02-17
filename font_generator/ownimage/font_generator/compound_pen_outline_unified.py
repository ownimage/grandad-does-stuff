from dataclasses import dataclass
from typing import List

from .pen_nib import PenNib
from .vector import Vector


@dataclass(frozen=True)
class CompoundPenOutlineRingUnified:
    nib: PenNib
    points: List[Vector]
    edge: float  # thickness of the black border

    def svg_paths(self) -> str:
        if len(self.points) < 2:
            return ""

        # Build inner nib (inset)
        inner_width  = max(0.0, self.nib.width     - 2 * self.edge)
        inner_thick  = max(0.0, self.nib.thickness - 2 * self.edge)
        inner_nib = PenNib(inner_width, inner_thick, self.nib.angle, pos=Vector(0, 0))

        outer_pts = []
        inner_pts = []

        # Collect ALL nib corners across the whole stroke
        for p in self.points:
            n = self.nib.moved_to(p.x, p.y)
            outer_pts.extend([n.tl, n.tr, n.br, n.bl])

            i = inner_nib.moved_to(p.x, p.y)
            inner_pts.extend([i.tl, i.tr, i.br, i.bl])

        # Compute unified hulls
        outer_hull = self._hull(outer_pts)
        inner_hull = self._hull(inner_pts)

        if not outer_hull or not inner_hull:
            return ""

        def path(points: List[Vector]) -> str:
            return (
                f"M {points[0].x} {points[0].y} "
                + " ".join(f"L {p.x} {p.y}" for p in points[1:])
                + " Z"
            )

        outer_d = path(outer_hull)
        inner_d = path(inner_hull)

        # Outer black shape
        svg = f'<path d="{outer_d}" fill="black" stroke="none" />\n'
        # Inner white hole
        svg += f'<path d="{inner_d}" fill="white" stroke="none" />\n'

        return svg

    def _hull(self, pts: List[Vector]) -> List[Vector]:
        pts = sorted(pts, key=lambda p: (p.x, p.y))

        def cross(o, a, b):
            return (a.x - o.x)*(b.y - o.y) - (a.y - o.y)*(b.x - o.x)

        lower = []
        for p in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        upper = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        return lower[:-1] + upper[:-1]