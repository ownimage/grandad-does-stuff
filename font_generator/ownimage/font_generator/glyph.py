from typing import List
from vector2d import Vector2D

from ownimage.font_generator.mark import Mark


class Glyph:
    def __init__(self, vec: Vector2D, marks: List[Mark]):
        self.vec = vec
        self.marks = marks

    def svg(self, posn: Vector2D, scale: float, pen_thickness: float):
        svg = ""
        for mark in self.marks:
            svg += mark.svg(posn.__add__(self.vec), scale, pen_thickness)
        return svg
