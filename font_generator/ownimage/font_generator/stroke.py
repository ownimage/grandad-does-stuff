from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union, List

from .font_parameters import FontParameters
from .nib import Nib
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


    def point_at(self, t: float) -> Vector:
        return self.vec * t

    def bl(self, fp: FontParameters) -> Vector:
        nib = Nib.from_font_parameters(fp)
        return self.vec + nib.bl

    def tr(self, fp: FontParameters) -> Vector:
        nib = Nib.from_font_parameters(fp)
        return nib.tr

    def tl(self, fp: FontParameters) -> Vector:
        nib = Nib.from_font_parameters(fp)
        return nib.tl

    def br(self, fp: FontParameters) -> Vector:
        nib = Nib.from_font_parameters(fp)
        return self.vec + nib.br

    def make_width(self, width: float, fp: FontParameters) -> Stroke:
        current = self.br(fp).x - self.tl(fp).x
        delta = width - current
        return Stroke(self.vec + Vector(delta, 0))
