from __future__ import annotations
from dataclasses import dataclass, field

import math

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .pen_nib import PenNib
from .pen_stroke import PenStroke
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector import Vector
from .vector_math import VectorMath as VM

@dataclass(frozen=True)
class Stroke(Strokeable):
    vec: Vector
    stroke_type: StrokeType = StrokeType.Block
    direction: Vector = field(init=False)

    def __post_init__(self):
        direction = self.vec.normalized()
        object.__setattr__(self, "direction", direction)


    def __add__(self, other):
        from .compound_stroke import CompoundStroke
        from .stroke_line import StrokeLine

        if isinstance(other, (Stroke, StrokeLine)):
            return CompoundStroke([self, other])

        if isinstance(other, CompoundStroke):
            return CompoundStroke(other.strokes + [self])


        raise NotImplemented


    @staticmethod
    def from_xy(x: float, y: float, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(Vector(x, y), stroke_type)

    @staticmethod
    def between(start: Vector, end: Vector, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(start - end, stroke_type)

    @staticmethod
    def down(length: float, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(Vector(0, -length), stroke_type)

    @staticmethod
    def right(length: float, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(Vector(length, 0), stroke_type)

    def extend(self, e: Stroke | Vector | float) -> Stroke:
        if isinstance(e, Stroke):
            if e.stroke_type == StrokeType.Extend:
                return Stroke(self.vec + e.vec, self.stroke_type)
            raise RuntimeError("Can only extend by a Stroke of type Extend.")

        if isinstance(e, Vector):
            return Stroke(self.vec + e, self.stroke_type)

        if isinstance(e, float):
            return Stroke(self.vec + e * self.direction, self.stroke_type)

        raise RuntimeError(f"Extension type of {type(e)}.")


    def get_geom(self, start: Vector, fp: FontParameters, scale: float, before: Strokeable, after: Strokeable, geom_set: GeometrySet):
        if self.stroke_type == StrokeType.Block or self.stroke_type == StrokeType.Line:
            start_nib = PenNib.from_font_parameters(fp)
            end_nib = start_nib.move(self.vec)
            pen_stroke = PenStroke(start_nib, end_nib)
            pen_stroke.get_geom(start, scale, geom_set)

        return start + self.vec

    def bl(self, fp: FontParameters):
        nib = PenNib.from_font_parameters(fp)
        return self.vec + nib.bl

    def tr(self, fp: FontParameters):
        nib = PenNib.from_font_parameters(fp)
        return nib.tr