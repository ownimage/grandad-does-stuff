from typing import List
from vector2d import Vector2D

from .stroke import Stroke


class Mark:
    def __init__(self, vec: Vector2D, strokes: List[Stroke]):
        self.vec = vec
        self.strokes = strokes

    def svg(self, posn: Vector2D, scale: float, pen_thickness: float):
        start = posn.__add__(self.vec)
        svg = ""
        for stroke in self.strokes:
            start, line = stroke.svg(start, scale, pen_thickness)
            svg = svg + line

        return svg + "\n"

    def birdfont_path(self, scale: float, pen_thickness: float):
        start = self.vec
        paths = []
        for stroke in self.strokes:
            start, stroke_paths = stroke.birdfont_path(start, scale, pen_thickness)
            paths += stroke_paths

        return paths