from dataclasses import dataclass
from typing import List

from .pen_nib import PenNib
from .vector import Vector


@dataclass(frozen=True)
class CompoundPenOutline:
    nib: PenNib
    points: List[Vector]

    def svg_path(self) -> str:
        if len(self.points) < 2:
            return ""

        paths: List[str] = []

        for i in range(len(self.points) - 1):
            p0 = self.points[i]
            p1 = self.points[i + 1]

            n0 = self.nib.moved_to(p0.x, p0.y)
            n1 = self.nib.moved_to(p1.x, p1.y)

            # 8 corners: 4 from each nib
            pts = [
                n0.tl, n0.tr, n0.br, n0.bl,
                n1.tl, n1.tr, n1.br, n1.bl,
            ]

            # Convex hull of the 8 points gives the segment outline
            hull = self._hull(pts)
            if not hull:
                continue

            d = f"M {hull[0].x} {hull[0].y} " + " ".join(
                f"L {p.x} {p.y}" for p in hull[1:]
            ) + " Z"

            paths.append(f'<path d="{d}" fill="black" stroke="none" />')

        return "\n".join(paths)

    def _hull(self, pts: List[Vector]) -> List[Vector]:
        # Monotone chain convex hull
        pts = sorted(pts, key=lambda p: (p.x, p.y))

        def cross(o: Vector, a: Vector, b: Vector) -> float:
            return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

        lower: List[Vector] = []
        for p in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        upper: List[Vector] = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        return lower[:-1] + upper[:-1]
