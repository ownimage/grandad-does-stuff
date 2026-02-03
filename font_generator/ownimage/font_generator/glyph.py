from typing import List
from vector2d import Vector2D

from .font_parameters import FontParameters
from .mark import Mark


class Glyph:
    def __init__(self, vec: Vector2D, marks: List[Mark]):
        self.vec = vec
        self.marks = marks

    def svg(self, posn: Vector2D, fp: FontParameters, scale: float):
        svg = ""
        for mark in self.marks:
            svg += mark.svg(posn.__add__(self.vec), fp, scale)
        return svg

    def birdfont_path(self, scale: float, pen_thickness: float):
        paths = []
        for mark in self.marks:
            paths += mark.birdfont_path(scale, pen_thickness)
        return paths
