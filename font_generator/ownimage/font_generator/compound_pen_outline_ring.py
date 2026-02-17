from dataclasses import dataclass
from typing import List

from .pen_nib import PenNib
from .vector import Vector


@dataclass(frozen=True)
class CompoundPenOutlineRing:
    nib: PenNib
    points: List[Vector]
    edge: float  # desired edge thickness

    def svg_paths(self) -> str:
        if len(self.points) < 2:
            return ""

        paths: List[str] = []

        # Inner nib: inset by `edge` on all sides
        inner_width = max(0.0, self.nib.width - 2 * self.edge)
        inner_thick = max(0.0, self.nib.thickness - 2 * self.edge)
        inner_nib = PenNib(inner_width, inner_thick, self.nib.angle, pos=Vector(0, 0))

        for i in range(len(self.points) - 1):
            p0 = self.points[i]
            p1 = self.points[i + 1]

            # Outer hull (current behaviour)
            n0 = self.nib.moved_to(p0.x, p0.y)
            n1 = self.nib.moved_to(p1.x, p1.y)
            outer_pts = [
                n0.tl, n0.tr, n0.br, n0.bl,
                n1.tl, n1.tr, n1.br, n1.bl,
            ]
            outer_hull = self._hull(outer_pts)

            # Inner hull (inset nib)
            i0 = inner_nib.moved_to(p0.x, p0.y)
            i1 = inner_nib.moved_to(p1.x, p1.y)
            inner_pts = [
                i0.tl, i0.tr, i0.br, i0.bl,
                i1.tl, i1.tr, i1.br, i1.bl,
            ]
            inner_hull = self._hull(inner_pts)

            if not outer_hull or not inner_hull:
                continue

            def path_from(points: List[Vector]) -> str:
                return (
                    f"M {points[0].x} {points[0].y} "
                    + " ".join(f"L {p.x} {p.y}" for p in points[1:])
                    + " Z"
                )

            outer_d = path_from(outer_hull)
            inner_d = path_from(inner_hull)

            # Outer black polygon
            paths.append(f'<path d="{outer_d}" fill="black" stroke="none" />')
            # Inner white polygon on top
            paths.append(f'<path d="{inner_d}" fill="white" stroke="none" />')

        return "\n".join(paths)

    def _hull(self, pts: List[Vector]) -> List[Vector]:
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