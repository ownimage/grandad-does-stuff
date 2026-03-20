from __future__ import annotations

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .stroke_type import StrokeType
from .vector import Vector

class Strokeable:

    def __init__(self, stroke_type: StrokeType = StrokeType.Block):
        self.stroke_type = stroke_type

    def _not_implemented(self, name: str) -> None:
        raise RuntimeError(f"{name}() not implemented in {self.__class__.__name__}")

    def start(self) -> Vector:
        return Vector(0, 0)

    def geometry(self, fp: FontParameters, start: Vector, scale: float, before: Strokeable, after: Strokeable, geom_set: GeometrySet) -> Vector:
        self._not_implemented("geometry")

    def bounding_box(self, fp: FontParameters, start: Vector = Vector(0, 0), scale: float = 1.0):
        geom_set = GeometrySet()
        self.geometry(fp, start, scale, None, None, geom_set)
        return geom_set.bounding_box()

    def svg(self, start: Vector, fp: FontParameters, scale: float) -> str:
        self._not_implemented("svg")

    def birdfont_path(self, start: Vector, fp: FontParameters, scale: float) -> list:
        self._not_implemented("birdfont_path")

    def advance(self, pos: Vector) -> Vector:
        return pos + self.vec