from __future__ import annotations

import math

from .compound_stroke import CompoundStroke
from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector import Vector
from .vector_math import VectorMath as VM


class StrokeLine(Strokeable):

    def __init__(self, vec: Vector):
        super().__init__(StrokeType.Line)
        self.vec = vec

    @staticmethod
    def from_xy(x: float, y: float):
        return StrokeLine(Vector(x, y))

    @staticmethod
    def between(start: Vector, end: Vector) -> StrokeLine:
        return StrokeLine(start - end)

    @staticmethod
    def right(lenght: float) -> StrokeLine:
        return StrokeLine(Vector(lenght, 0))

    def extend(self, e: StrokeLine) -> StrokeLine:
        if e.stroke_type != StrokeType.Extend:
            raise RuntimeError("Stroke of wrong type.")
        return StrokeLine(self.vec + e.vec)

    def get_geom(self, start: Vector, fp: FontParameters, scale: float, prev: Strokeable, next: Strokeable, geom_set: GeometrySet):
        unit = self.vec.normalized()
        offset = unit.rotated(90) * fp.line_thickness * fp.pen_thickness * scale * .5
        p1 = start * scale
        p2 = (start + self.vec) * scale
        p3 = p2 + offset
        p4 = p1 + offset
        geom_set.get_current_outline().extend([p3, p4, p1, p2])
        geom_set.add_new_outline()
        geom_set.add_new_hole()
        return start + self.vec
