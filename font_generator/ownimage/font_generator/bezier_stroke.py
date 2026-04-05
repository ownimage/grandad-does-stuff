from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union, Tuple

from .cubic_bezier import CubicBezier
from .font_parameters import FontParameters
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
    def from_four_points(
            p0: Union[Vector, Tuple[float, float]],
            p1: Union[Vector, Tuple[float, float]],
            p2: Union[Vector, Tuple[float, float]],
            p3: Union[Vector, Tuple[float, float]],
            fp: FontParameters = None,
            debug_visual: bool = False,
    ) -> BezierStroke:
        p0, p1, p2, p3 = map(Vector.of, (p0, p1, p2, p3))
        bezier = CubicBezier(p0, p1, p2, p3)
        num_samples = 20 if fp is None else fp.bezier_samples
        return BezierStroke(bezier, num_samples, debug_visual)

    @staticmethod
    def from_three_points(
            p0: Union[Vector, Tuple[float, float]],
            p1: Union[Vector, Tuple[float, float]],
            p2: Union[Vector, Tuple[float, float]],
            fp: FontParameters = None,
            debug_visual: bool = False,
    ) -> BezierStroke:
        p0, p1, p2 = map(Vector.of, (p0, p1, p2))
        bezier = CubicBezier.from_three_points(p0, p1, p2)
        num_samples = 20 if fp is None else fp.bezier_samples
        return BezierStroke(bezier, num_samples, debug_visual)

    @staticmethod
    def bezier_through(
            p0: Union[Vector, Tuple[float, float]],
            p1: Union[Vector, Tuple[float, float]],
            p2: Union[Vector, Tuple[float, float]],
            p3: Union[Vector, Tuple[float, float]],
            fp: FontParameters = None,
            debug_visual: bool = False,
    ) -> BezierStroke:
        p0, p1, p2, p3 = map(Vector.of, (p0, p1, p2, p3))
        bezier = CubicBezier.bezier_through(p0, p1, p2, p3)
        num_samples = 20 if fp is None else fp.bezier_samples
        return BezierStroke(bezier, num_samples, debug_visual)

    @staticmethod
    def horizontal_flourish(
            length: float,
            offset: float,
            x_start: float = 0,
            fp: FontParameters = None,
            debug_visual: bool = False,
    ) -> BezierStroke:
        return BezierStroke.bezier_through(
            (x_start, 0),
            (x_start + length / 4, offset),
            (x_start + 3 * length / 4, -offset),
            (x_start + length, 0),
            fp,
            debug_visual
        )

    def point_at(self, t: float) -> Vector:
        return self.bezier.point_at(t)

    def y_at_x(self, x: float):
        return self.bezier.y_at_x(x)

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
        return pos + self.bezier.p3
