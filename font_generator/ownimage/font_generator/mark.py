from __future__ import annotations

from typing import List
from shapely.geometry import Point

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .stroke import Strokeable

from .vector_math import VectorMath as VM


class Mark:
    def __init__(self, vec: Point, strokes: List[Strokeable] | Strokeable):
        self.vec = vec
        self.strokes: List[Strokeable] = [strokes] if isinstance(strokes, Strokeable) else strokes

    def svg(self, posn: Point, fp: FontParameters, scale: float):
        start = Point(posn.x + self.vec.x, posn.y + self.vec.y)
        geom_set = GeometrySet()
        for i in range(len(self.strokes)):
            prev_item = self.strokes[i - 1] if i > 0 else None
            curr_item = self.strokes[i]
            next_item = self.strokes[i + 1] if i < len(self.strokes) - 1 else None

            start = curr_item.get_geom(start, fp, scale, prev_item, next_item, geom_set)

        return geom_set.svg(fp.filled) + "\n"

    def birdfont_path(self, fp: FontParameters, scale: float):
        start = self.vec
        paths = []
        for stroke in self.strokes:
            start, stroke_paths = stroke.birdfont_path(start, fp, scale)
            paths += stroke_paths

        return paths

    def plus(self, off: Point) -> Mark:
        return Mark(VM.add_points(self.vec, off), self.strokes)
