from typing import List
from shapely.geometry import Point

from .font_parameters import FontParameters
from .mark import Mark


class Glyph:
    def __init__(self, vec: Point, marks: List[Mark]):
        self.vec = vec
        self.marks = marks

    def svg(self, posn: Point, fp: FontParameters, scale: float):
        svg = ""
        for mark in self.marks:
            svg += mark.svg(Point(posn.x + self.vec.x, posn.y + self.vec.y), fp, scale)
        return svg

    def birdfont_path(self, scale: float, pen_thickness: float):
        paths = []
        for mark in self.marks:
            paths += mark.birdfont_path(scale, pen_thickness)
        return paths
