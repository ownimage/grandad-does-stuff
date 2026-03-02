from __future__ import annotations

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .stroke_type import StrokeType
from .vector import Vector

class Strokeable:

    def __init__(self, stroke_type: StrokeType = StrokeType.Block):
        self.stroke_type = stroke_type

    def _not_implemented(self, name: str):
        raise RuntimeError(f"{name}() not implemented in {self.__class__.__name__}")

    def get_geom(self, start, fp, scale, prev, next, geom_set):
        self._not_implemented("get_geom")

    def svg(self, start, fp, scale):
        self._not_implemented("svg")

    def birdfont_path(self, start, fp, scale):
        self._not_implemented("birdfont_path")