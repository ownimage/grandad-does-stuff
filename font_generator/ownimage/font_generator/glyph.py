from typing import List

from .font_parameters import FontParameters
from .mark import Mark
from .vector import Vector


class Glyph:
    def __init__(self, marks: List[Mark], fp: FontParameters):
        self.marks = marks

        union = None
        for m in self.marks:
            bb = m.bounding_box(fp)
            union = bb if union is None else union.union(bb)

        self.vec = Vector(-union.left , 0)
        self.width = union.width

    def svg(self, start: Vector, fp: FontParameters, scale: float):
        svg = ""
        for mark in self.marks:
            svg += mark.svg(fp, Vector(start.x + self.vec.x, start.y + self.vec.y), scale)
        return svg

    def birdfont_path(self, fp: FontParameters, scale: float):
        paths = []
        for mark in self.marks:
            paths += mark.birdfont_path(fp, scale)
        return paths
