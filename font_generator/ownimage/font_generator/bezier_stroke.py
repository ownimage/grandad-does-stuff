from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from shapely.geometry import Polygon
from shapely.geometry.multipoint import MultiPoint
from shapely.ops import unary_union

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .pen_nib import PenNib
from .pen_stroke import PenStroke
from .bezier import CubicBezier
from .stroke import Stroke
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
        if self.num_samples < 4:
            raise ValueError("num_samples must be at least 4")

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
        def add_start_and_scale(pt: Vector) -> Vector:
            return Stroke.add_start_and_scale(pt, start, scale)

        points = self._sample_points()
        nib = PenNib.from_font_parameters(fp)
        top: List[Vector] = []
        bottom: List[Vector] = []
        outline = None

        for i in range(len(points)-1):
            n1 = nib.at(points[i])
            n2 = nib.at(points[i+1])
            p = [add_start_and_scale(p).xy() for p in n1.corners() + n2.corners()]
            h = MultiPoint(p).convex_hull

            if outline is None:
                outline = h
            else:
                outline = unary_union([outline, h])

        pts = list(outline.exterior.coords)
        outline = [Vector(p[0], p[1]) for p in pts]
        geom_set.replace_current_outline(outline)
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
