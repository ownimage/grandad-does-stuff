from __future__ import annotations

import math

from .compound_stroke import CompoundStroke
from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .stroke import Stroke
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
    def right(length: float) -> StrokeLine:
        return StrokeLine(Vector(length, 0))

    @staticmethod
    def down(length: float) -> StrokeLine:
        return StrokeLine(Vector(0, -length))

    def extend(self, e: StrokeLine) -> StrokeLine:
        if isinstance(e, Stroke):
            if e.stroke_type == StrokeType.Extend:
                return StrokeLine(self.vec + e.vec)
            raise RuntimeError("Can only extend by a Stroke of type Extend.")

        if isinstance(e, Vector):
            return StrokeLine(self.vec + e)

        if isinstance(e, float):
            return StrokeLine(self.vec + e * self.vec.normalized())

        raise RuntimeError(f"Extension type of {type(e)}.")

    def get_geom(self, start: Vector, fp: FontParameters, scale: float, prev: Strokeable, next: Strokeable, geom_set: GeometrySet):
        unit = self.vec.normalized()
        offset = unit.rotated(90) * fp.pen_thickness * scale
        p1 = start * scale + offset * 0.5
        p2 = (start + self.vec) * scale + offset * 0.5
        p3 = p2 - offset
        p4 = p1 - offset
        geom_set.replace_current_outline([p3, p4, p1, p2])
        geom_set.add_new_outline()
        geom_set.add_new_hole()
        return start + self.vec
