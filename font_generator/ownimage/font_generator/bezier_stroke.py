from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .pen_nib import PenNib
from .pen_stroke import PenStroke
from .bezier import CubicBezier
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector import Vector


@dataclass(frozen=True)
class BezierStroke(Strokeable):
    bezier: CubicBezier = field(default_factory=lambda: CubicBezier(Vector(0, 0), Vector(0, 0), Vector(0, 0), Vector(0, 0)))
    num_samples: int = 20
    debug_visual: bool = False

    def __post_init__(self):
        object.__setattr__(self, "stroke_type", StrokeType.Block)

    @staticmethod
    def from_three_points(
        p0: Vector,
        p1: Vector,
        p2: Vector,
        num_samples: int = 20,
        debug_visual: bool = False,
    ) -> BezierStroke:
        bezier = CubicBezier.from_three_points(p0, p1, p2)
        return BezierStroke(bezier, num_samples, debug_visual)

    def _sample_points(self) -> List[Vector]:
        """Sample points along the curve at evenly spaced t values."""
        num_points = self.num_samples
        if num_points < 1:
            return []
        if num_points == 1:
            return [self.bezier.point_at(0.5)]
        if num_points == 2:
            return [self.bezier.point_at(0), self.bezier.point_at(1)]

        points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            points.append(self.bezier.point_at(t))
        return points

    def _interpolate(self, arr: List[tuple[float, Vector]], t: float) -> Vector:
        """Interpolate values from a sorted array to find value at t."""
        if t <= arr[0][0]:
            return arr[0][1]
        if t >= arr[-1][0]:
            return arr[-1][1]

        for i in range(len(arr) - 1):
            t0, v0 = arr[i]
            t1, v1 = arr[i + 1]
            if t0 <= t <= t1:
                alpha = (t - t0) / (t1 - t0) if t1 != t0 else 0.0
                return v0 + (v1 - v0) * alpha

        return arr[-1][1]

    def geometry(
        self,
        start: Vector,
        fp: FontParameters,
        scale: float,
        before: Strokeable,
        after: Strokeable,
        geom_set: GeometrySet
    ) -> Vector:
        """
        Generate geometry by interpolating the nib along the curve
        and approximating it with short PenStroke segments.
        """
        points = self._sample_points()

        if len(points) < 2:
            return start + self.bezier.p3 - self.bezier.p0

        nib = PenNib.from_font_parameters(fp)
        tl: List[tuple[float, Vector]] = []
        tr: List[tuple[float, Vector]] = []
        bl: List[tuple[float, Vector]] = []
        br: List[tuple[float, Vector]] = []
        nibs: List[PenNib] = []

        for i in range(len(points)):
            n = nib.at(points[i])
            nibs.append(n)

            t_tl = self.bezier.closet_t_to(n.tl)
            tl.append((t_tl, n.tl))

            t_tr = self.bezier.closet_t_to(n.tr)
            tr.append((t_tr, n.tr))

            t_bl = self.bezier.closet_t_to(n.bl)
            bl.append((t_bl, n.bl))

            t_br = self.bezier.closet_t_to(n.br)
            br.append((t_br, n.br))

        tl.sort(key=lambda x: x[0])
        tr.sort(key=lambda x: x[0])
        bl.sort(key=lambda x: x[0])
        br.sort(key=lambda x: x[0])

        for i in range(len(nibs) - 1):
            pen_stroke = PenStroke(nibs[i], nibs[i + 1])
            segment_before = before if i == 0 else self
            segment_after = after if i == len(nibs) - 2 else self
            pen_stroke.geometry(Vector(0, 0), scale, segment_before, segment_after, geom_set)

        return start + self.bezier.p3 - self.bezier.p0

    def svg(self, start: Vector, fp: FontParameters, scale: float) -> str:
        p0 = (start + self.bezier.p0) * scale
        p1 = (start + self.bezier.p1) * scale
        p2 = (start + self.bezier.p2) * scale
        p3 = (start + self.bezier.p3) * scale
        return f"M {p0.x},{p0.y} C {p1.x},{p1.y} {p2.x},{p2.y} {p3.x},{p3.y}"

    def birdfont_path(self, start: Vector, fp: FontParameters, scale: float):
        p0 = (start + self.bezier.p0) * scale
        p1 = (start + self.bezier.p1) * scale
        p2 = (start + self.bezier.p2) * scale
        p3 = (start + self.bezier.p3) * scale
        return (p0, f"C {p1.x},{p1.y} {p2.x},{p2.y} {p3.x},{p3.y}")

    def advance(self, pos: Vector) -> Vector:
        return pos + self.bezier.p3 - self.bezier.p0
