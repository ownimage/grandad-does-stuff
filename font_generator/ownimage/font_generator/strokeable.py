from __future__ import annotations

from typing import Union

from shapely.geometry.multipoint import MultiPoint
from shapely.ops import unary_union

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .nib import Nib
from .stroke_type import StrokeType
from .vector import Vector
from .vector_list import VectorList


class Strokeable:

    def __init__(self, stroke_type: StrokeType = StrokeType.Block, num_samples: int = 20):
        self.stroke_type = stroke_type
        self.num_samples = num_samples

    def __add__(self, other: Union['Stroke', 'BezierStroke', 'CompoundStroke']) -> 'CompoundStroke':
        from .stroke import Stroke
        from .bezier_stroke import BezierStroke
        from .compound_stroke import CompoundStroke

        if isinstance(other, (Stroke, BezierStroke)):
            return CompoundStroke([self, other])

        if isinstance(other, CompoundStroke):
            return CompoundStroke([self] + other.strokes)

        raise NotImplementedError(f"Cannot add {type(other)} to Strokeable")

    def _not_implemented(self, name: str) -> None:
        raise RuntimeError(f"{name}() not implemented in {self.__class__.__name__}")

    def start(self) -> Vector:
        return Vector(0, 0)

    def sample_points(self, num_samples: int = 20) -> list[Vector]:
        self._not_implemented("sample_points")
        return None

    def point_at(self, t: float) -> Vector:
        self._not_implemented("point_at")
        return None

    def geometry(self, fp: FontParameters, start: Vector, scale: float, before: 'Strokeable | None', after: 'Strokeable | None', geom_set: GeometrySet) -> Vector:
        def add_start_and_scale(pt: Vector) -> Vector:
            # Import Stroke here to avoid circular import issues
            from .stroke import Stroke  
            return Stroke.add_start_and_scale(pt, start, scale)

        if self.stroke_type not in {StrokeType.Move, StrokeType.Extend}:
            points = self.sample_points(self.num_samples)
            nib = Nib.from_font_parameters(fp)
            geom_set.add_new_outline()
            outline = None

            for i in range(len(points) - 1):
                n1 = nib.at(points[i])
                n2 = nib.at(points[i + 1])
                p = [add_start_and_scale(p).xy() for p in n1.outline() + n2.outline()]
                h = MultiPoint(p).convex_hull
                outline = unary_union([outline, h])

            outline = VectorList.from_list_of_tuples(list(outline.exterior.coords))
            geom_set.replace_current_outline(outline)
            geom_set.add_new_outline()
            geom_set.add_new_hole()
        return self.advance(start)

    def advance(self, pos: Vector) -> Vector:
        return pos + self.vec