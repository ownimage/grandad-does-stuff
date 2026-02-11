from typing import List

from .font_parameters import FontParameters
from .mark import Mark
from .vector import Vector

class Glyph:
    def __init__(self, vec: Vector, marks: List[Mark], width):
        self.vec = vec
        self.marks = marks
        self.width = width

    def svg(self, posn: Vector, fp: FontParameters, scale: float):
        svg = ""
        for mark in self.marks:
            svg += mark.svg(Vector(posn.x + self.vec.x, posn.y + self.vec.y), fp, scale)
        return svg

    def birdfont_path(self, fp: FontParameters, scale: float):
        paths = []
        for mark in self.marks:
            paths += mark.birdfont_path(fp, scale)
        return paths
