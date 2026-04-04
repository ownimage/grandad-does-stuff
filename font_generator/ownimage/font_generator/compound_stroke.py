from __future__ import annotations

from typing import List, Union

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .stroke import Stroke
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector import Vector
from .vector_math import VectorMath as VM


class CompoundStroke(Strokeable):
    def __init__(self, strokes: Union[Strokeable, List[Strokeable]]):
        self.strokes: list[Strokeable] = [strokes] if isinstance(strokes, Strokeable) else strokes
        super().__init__(self.strokes[0].stroke_type)

    def __add__(self, other: Union[CompoundStroke, Strokeable]) -> CompoundStroke:
        if isinstance(other, CompoundStroke):
            return CompoundStroke(self.strokes + other.strokes)

        if isinstance(other, Strokeable):
            return CompoundStroke(self.strokes + [other])

        raise NotImplemented

    def add_after(self, cs: CompoundStroke) -> CompoundStroke:
        cs_first = cs.strokes[0]
        new_list = self.strokes.copy()
        if isinstance(cs_first, Stroke) and cs_first.stroke_type == StrokeType.Extend:
            last_stroke = new_list.pop()
            new_stroke = Stroke(last_stroke.vec + cs_first.vec, last_stroke.stroke_type)
            new_list.append(new_stroke)
            new_list += cs.strokes[1:]
        else:
            new_list += cs.strokes
        return CompoundStroke(new_list)

    def geometry(self, fp: FontParameters, start: Vector, scale: float, before: Strokeable, after: Strokeable, geom_set: GeometrySet) -> Vector:
        current_pos = start
        for stroke in self.strokes:
            current_pos = stroke.geometry(fp, current_pos, scale, before, after, geom_set)
        return current_pos

    def svg(self, start: Vector, fp: FontParameters, scale: float) -> str:
        svg = ""
        current_pos = start
        for stroke in self.strokes:
            current_pos, s = stroke.svg(current_pos, fp, scale)
            svg += s
        return svg

    def birdfont_path(self, start: Vector, fp: FontParameters, scale: float) -> list:
        paths = []
        current_pos = start
        for stroke in self.strokes:
            current_pos, new_paths = stroke.birdfont_path(current_pos, fp, scale)
            paths += new_paths
        return paths
