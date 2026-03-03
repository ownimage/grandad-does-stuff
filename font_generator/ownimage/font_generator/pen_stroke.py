from dataclasses import dataclass

from .geometry_set import GeometrySet
from .pen_nib import PenNib
from .vector import Vector
from .vector_math import VectorMath as VM


@dataclass(frozen=True)
class PenStroke:
    start: PenNib
    end: PenNib

    def get_geom(self, start: Vector, scale: float, geom_set: GeometrySet) -> GeometrySet:
        dpl = VM.distance_point_to_line

        def add_start_and_scale(pt: Vector) -> Vector:
            return (pt + start) * scale

        outline = [add_start_and_scale(self.start.tl)]

        if dpl(self.start.pos, self.end.pos, self.start.bl) > dpl(self.start.pos, self.end.pos, self.start.tl):
            outline.append(add_start_and_scale(self.start.bl))

        if dpl(self.start.pos, self.end.pos, self.end.tl) > dpl(self.start.pos, self.end.pos, self.end.bl):
            outline.append(add_start_and_scale(self.end.tl))

        outline.append(add_start_and_scale(self.end.bl))
        outline.append(add_start_and_scale(self.end.br))

        if dpl(self.start.pos, self.end.pos, self.end.tr) > dpl(self.start.pos, self.end.pos, self.end.br):
            outline.append(add_start_and_scale(self.end.tr))

        if dpl(self.start.pos, self.end.pos, self.start.br) > dpl(self.start.pos, self.end.pos, self.start.tr):
            outline.append(add_start_and_scale(self.start.br))

        outline.append(add_start_and_scale(self.start.tr))

        geom_set.add_new_outline(outline)
        geom_set.add_new_hole()
        return geom_set
