from typing import List
from vector2d import Vector2D

from .font_parameters import FontParameters
from .stroke import Strokeable


class Mark:
    def __init__(self, vec: Vector2D, strokes: List[Strokeable]):
        self.vec = vec
        self.strokes = strokes

    def svg(self, posn: Vector2D, fp: FontParameters, scale: float):
        start = posn.__add__(self.vec)
        svg = ""
        for stroke in self.strokes:
            start, line = stroke.svg(start, fp, scale)
            svg += line

        return svg + "\n"

    def birdfont_path(self, scale: float, pen_thickness: float):
        start = self.vec
        paths = []
        for stroke in self.strokes:
            start, stroke_paths = stroke.birdfont_path(start, scale, pen_thickness)
            paths += stroke_paths

        return paths