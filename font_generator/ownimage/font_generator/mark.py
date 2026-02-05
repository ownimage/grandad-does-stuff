from typing import List
from shapely.geometry import Point

from .font_parameters import FontParameters
from .stroke import Strokeable


class Mark:
    def __init__(self, vec: Point, strokes: List[Strokeable]):
        self.vec = vec
        self.strokes = strokes

    def svg(self, posn: Point, fp: FontParameters, scale: float):
        start = Point(posn.x + self.vec.x, posn.y + self.vec.y)
        svg = ""
        for stroke in self.strokes:
            start, line = stroke.svg(start, fp, scale)
            svg += line

        return svg + "\n"

    def birdfont_path(self, fp: FontParameters,  scale: float):
        start = self.vec
        paths = []
        for stroke in self.strokes:
            start, stroke_paths = stroke.birdfont_path(start, fp, scale)
            paths += stroke_paths

        return paths