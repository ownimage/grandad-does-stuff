from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union, List

from .font_parameters import FontParameters
from .pen_nib import PenNib
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector import Vector


@dataclass(frozen=True)
class Stroke(Strokeable):
    vec: Vector
    stroke_type: StrokeType = StrokeType.Block
    direction: Vector = field(init=False)
    num_samples: int = 2

    def __post_init__(self):
        direction = self.vec.normalized()
        object.__setattr__(self, "direction", direction)

    def __add__(self, other: Union[Stroke, 'BezierStroke', 'CompoundStroke']) -> 'CompoundStroke':
        from .bezier_stroke import BezierStroke
        from .compound_stroke import CompoundStroke

        if isinstance(other, (Stroke, BezierStroke)):
            return CompoundStroke([self, other])

        if isinstance(other, CompoundStroke):
            return CompoundStroke([self] + other.strokes)

        raise NotImplementedError(f"Cannot add {type(other)} to Stroke")

    @staticmethod
    def from_xy(x: float, y: float, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(Vector(x, y), stroke_type)

    @staticmethod
    def between(start: Vector, end: Vector, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(start - end, stroke_type)

    @staticmethod
    def down(length: float = 1, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(Vector(0, -length), stroke_type)

    @staticmethod
    def right(length: float = 1.0, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(Vector(length, 0), stroke_type)

    @staticmethod
    def add_start_and_scale(pt: Vector, start: Vector, scale: float) -> Vector:
        return (pt + start) * scale

    def extend(self, e: Union[Stroke, Vector, float]) -> Stroke:
        if isinstance(e, Stroke):
            if e.stroke_type == StrokeType.Extend:
                return Stroke(self.vec + e.vec, self.stroke_type)
            raise RuntimeError("Can only extend by a Stroke of type Extend.")

        if isinstance(e, Vector):
            return Stroke(self.vec + e, self.stroke_type)

        if isinstance(e, float):
            return Stroke(self.vec + e * self.direction, self.stroke_type)

        raise RuntimeError(f"Extension type of {type(e)}.")

    def sample_points(self, num_samples: int = 20) -> List[Vector]:
        points = []
        for i in range(num_samples):
            t = i / (num_samples - 1)
            points.append(self.vec * t)
        return points

    def bl(self, fp: FontParameters) -> Vector:
        nib = PenNib.from_font_parameters(fp)
        return self.vec + nib.bl

    def tr(self, fp: FontParameters) -> Vector:
        nib = PenNib.from_font_parameters(fp)
        return nib.tr

    def tl(self, fp: FontParameters) -> Vector:
        nib = PenNib.from_font_parameters(fp)
        return nib.tl

    def br(self, fp: FontParameters) -> Vector:
        nib = PenNib.from_font_parameters(fp)
        return self.vec + nib.br

    def make_width(self, width: float, fp: FontParameters) -> Stroke:
        current = self.br(fp).x - self.tl(fp).x
        delta = width - current
        return Stroke(self.vec + Vector(delta, 0))
