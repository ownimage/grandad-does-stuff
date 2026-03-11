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
    def from_points(
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
            return start + self.bezier.p2 - self.bezier.p0

        nib = PenNib.from_font_parameters(fp)
        debug_segments: List[tuple[Vector, Vector]] = []

        for point in points:
            nib_at = nib.at(start + point)
            debug_segments.append((nib_at.l, nib_at.r))

        for i in range(len(points) - 1):
            segment_start = nib.at(start + points[i])
            segment_end = nib.at(start + points[i + 1])
            pen_stroke = PenStroke(segment_start, segment_end)

            segment_before = before if i == 0 else self
            segment_after = after if i == len(points) - 2 else self
            pen_stroke.geometry(Vector(0, 0), scale, segment_before, segment_after, geom_set)

        if self.debug_visual:
            for left, right in debug_segments:
                geom_set.graffiti.append([left * scale, right * scale])

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
