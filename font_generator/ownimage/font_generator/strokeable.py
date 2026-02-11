from __future__ import annotations

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .stroke_type import StrokeType
from .vector import Vector


class Strokeable:

    def __init__(self, stroke_type: StrokeType = StrokeType.Block):
        self.stroke_type = stroke_type

    def get_geom(self, start: Vector, fp: FontParameters, scale: float, prev: Strokeable, next: Strokeable, geom_set: GeometrySet):
        raise RuntimeError("Not implemented yet")

    def svg(self, start: Vector, fp: FontParameters, scale: float):
        raise RuntimeError("Not implemented yet")

    def birdfont_path(self, start: Vector, fp: FontParameters, scale: float):
        raise RuntimeError("Not implemented yet")
