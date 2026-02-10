from __future__ import annotations

from typing import List
from shapely.geometry import Point

from .font_parameters import FontParameters
from .stroke import Strokeable

from .vector_math import VectorMath as VM


class Mark:
    def __init__(self, vec: Point, strokes: List[Strokeable] | Strokeable):
        self.vec = vec
        self.strokes: List[Strokeable] = [strokes] if isinstance(strokes, Strokeable) else strokes

    def svg(self, posn: Point, fp: FontParameters, scale: float):
        start = Point(posn.x + self.vec.x, posn.y + self.vec.y)
        svg = ""
        for stroke in self.strokes:
            start, line = stroke.svg(start, fp, scale)
            svg += line

        return svg + "\n"

    def birdfont_path(self, fp: FontParameters, scale: float):
        start = self.vec
        paths = []
        for stroke in self.strokes:
            start, stroke_paths = stroke.birdfont_path(start, fp, scale)
            paths += stroke_paths

        return paths

    def plus(self, off: Point) -> Mark:
        return Mark(VM.add_points(self.vec, off), self.strokes)
