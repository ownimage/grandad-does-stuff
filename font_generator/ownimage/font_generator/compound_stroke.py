from __future__ import annotations

from shapely.geometry import Point

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .stroke import Stroke
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector_math import VectorMath as VM


class CompoundStroke(Strokeable):
    def __init__(self, strokes: Stroke | list[Stroke]):
        super().__init__()
        self.strokes: list[Stroke] = [strokes] if isinstance(strokes, Stroke) else strokes

    def get_geom(self, start: Point, fp: FontParameters, scale: float, prev: Strokeable, next: Strokeable, geom_set: GeometrySet):
        for i in range(len(self.strokes)):
            prev_item = self.strokes[i - 1] if i > 0 else None
            curr_item = self.strokes[i]
            next_item = self.strokes[i + 1] if i < len(self.strokes) - 1 else None

            start = curr_item.get_geom(start, fp, scale, prev_item, next_item, geom_set)
        return start

    def add_after(self, cs: CompoundStroke) -> CompoundStroke:
        cs_first = cs.strokes[0]
        new_list = self.strokes.copy()
        if isinstance(cs_first, Stroke) and cs_first.stroke_type == StrokeType.Extend:
            last_stroke = new_list.pop()
            new_stroke = Stroke(VM.add_points(last_stroke.vec, cs_first.vec), last_stroke.stroke_type)
            new_list.append(new_stroke)
            new_list += cs.strokes[1:]
        else:
            new_list += cs.strokes
        return CompoundStroke(new_list)

    def svg(self, posn: Point, fp: FontParameters, scale: float):
        svg = ""
        start = posn
        for stroke in self.strokes:
            start, s = stroke.svg(start, fp, scale)
            svg += s
        return start, svg

    def birdfont_path(self, start: Point, fp: FontParameters, scale: float):
        paths = []

        for stroke in self.strokes:
            start, new_paths = stroke.birdfont_path(start, fp, scale)
            paths += new_paths
        return start, paths
