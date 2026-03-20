from typing import List

from .font_parameters import FontParameters
from .mark import Mark
from .vector import Vector


class Glyph:
    def __init__(self, marks: List[Mark], fp: FontParameters):
        self.marks = marks

        left = min([mark.bounding_box(fp).left for mark in marks])
        right = max([mark.bounding_box(fp).right for mark in marks])

        self.vec = Vector(-left, 0)
        self.width = right - left

    def svg(self, posn: Vector, fp: FontParameters, scale: float):
        svg = ""
        for mark in self.marks:
            svg += mark.svg(fp, Vector(posn.x + self.vec.x, posn.y + self.vec.y), scale)
        return svg

    def birdfont_path(self, fp: FontParameters, scale: float):
        paths = []
        for mark in self.marks:
            paths += mark.birdfont_path(fp, scale)
        return paths
