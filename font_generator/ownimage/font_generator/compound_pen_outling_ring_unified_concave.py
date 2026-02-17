from dataclasses import dataclass
from typing import List

from .pen_nib import PenNib
from .vector import Vector


@dataclass(frozen=True)
class CompoundPenOutlineRingUnifiedConcave:
    nib: PenNib
    points: List[Vector]
    inset: float  # inward offset distance for the hole

    # ---------------------------------------------------------
    # 1. Compute union of convex polygons (nib rectangles)
    # ---------------------------------------------------------
    def polygon_union(self, polys: List[List[Vector]]) -> List[Vector]:
        # Start with first polygon
        result = polys[0]

        for poly in polys[1:]:
            result = self.union_two(result, poly)

        return result

    def union_two(self, A: List[Vector], B: List[Vector]) -> List[Vector]:
        # Sutherland–Hodgman polygon clipping (union via clipping complement)
        # But since all nib rectangles overlap heavily, we can use a simpler rule:
        # Keep all points from both polygons, then compute concave hull.
        pts = A + B
        return self.concave_hull(pts)

    # ---------------------------------------------------------
    # 2. Compute concave hull (k‑nearest‑neighbour algorithm)
    # ---------------------------------------------------------
    def concave_hull(self, pts: List[Vector], k: int = 3) -> List[Vector]:
        # Very small point sets → convex hull fallback
        if len(pts) < 4:
            return self.convex_hull(pts)

        # k must be >= 3
        k = max(3, min(k, len(pts) - 1))

        # Start with leftmost point
        start = min(pts, key=lambda p: (p.x, p.y))
        hull = [start]
        current = start
        prev_angle = 0

        while True:
            # Find k nearest neighbours
            neighbours = sorted(
                (p for p in pts if p != current),
                key=lambda p: (p.x - current.x)**2 + (p.y - current.y)**2
            )[:k]

            # Choose next point by smallest turning angle
            best = None
            best_angle = None

            for n in neighbours:
                angle = self.angle_between(current, n, prev_angle)
                if best is None or angle < best_angle:
                    best = n
                    best_angle = angle

            if best == start:
                break

            hull.append(best)
            prev_angle = best_angle
            current = best

        return hull

    def angle_between(self, a: Vector, b: Vector, prev_angle: float) -> float:
        import math
        dx = b.x - a.x
        dy = b.y - a.y
        ang = math.atan2(dy, dx)
        # Normalize relative to previous angle
        diff = ang - prev_angle
        while diff < 0:
            diff += 2 * math.pi
        return diff

    # ---------------------------------------------------------
    # 3. Convex hull (fallback)
    # ---------------------------------------------------------
    def convex_hull(self, pts: List[Vector]) -> List[Vector]:
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

    # ---------------------------------------------------------
    # 4. Inward offset of polygon
    # ---------------------------------------------------------
    def inset_polygon(self, poly: List[Vector], d: float) -> List[Vector]:
        # Simple inward offset: move each vertex inward along averaged normals
        inset = []
        n = len(poly)

        for i in range(n):
            p_prev = poly[(i - 1) % n]
            p_curr = poly[i]
            p_next = poly[(i + 1) % n]

            # Edge normals
            e1 = (p_curr - p_prev).normalized()
            e2 = (p_next - p_curr).normalized()

            n1 = Vector(-e1.y, e1.x)
            n2 = Vector(-e2.y, e2.x)

            # Average inward normal
            avg = (n1 + n2).normalized()

            inset.append(p_curr - avg * d)

        return inset

    # ---------------------------------------------------------
    # 5. SVG output
    # ---------------------------------------------------------
    def svg_paths(self) -> str:
        # Build all nib rectangles
        nib_polys = []
        for p in self.points:
            n = self.nib.moved_to(p.x, p.y)
            nib_polys.append([n.tl, n.tr, n.br, n.bl])

        # Union → concave outer boundary
        outer = self.polygon_union(nib_polys)

        # Inset → concave inner boundary
        inner = self.inset_polygon(outer, self.inset)

        def path(poly):
            return (
                f"M {poly[0].x} {poly[0].y} "
                + " ".join(f"L {p.x} {p.y}" for p in poly[1:])
                + " Z"
            )

        return (
            f'<path d="{path(outer)}" fill="black" stroke="none" />\n'
            f'<path d="{path(inner)}" fill="white" stroke="none" />\n'
        )