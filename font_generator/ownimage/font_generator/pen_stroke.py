from dataclasses import dataclass

from .pen_nib import PenNib
from .vector import Vector


@dataclass(frozen=True)
class PenStroke:
    start: PenNib
    end: PenNib

    def _hull(self, pts: list[Vector]) -> list[Vector]:
        # Monotone chain convex hull
        pts = sorted(pts, key=lambda p: (p.x, p.y))

        def cross(o: Vector, a: Vector, b: Vector) -> float:
            return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

        lower: list[Vector] = []
        for p in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        upper: list[Vector] = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        # last point of each list is the start of the other list
        return lower[:-1] + upper[:-1]

    def svg_path(self) -> str:
        # All 8 corners from both nibs
        pts = [
            self.start.tl, self.start.tr, self.start.br, self.start.bl,
            self.end.tl,   self.end.tr,   self.end.br,   self.end.bl,
        ]

        hull = self._hull(pts)
        if not hull:
            return ""

        d = f"M {hull[0].x} {hull[0].y} " + " ".join(
            f"L {p.x} {p.y}" for p in hull[1:]
        ) + " Z"

        return f'<path d="{d}" fill="black" stroke="none" />'