from dataclasses import dataclass

from .geometry_set import GeometrySet
from .pen_nib import PenNib
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector import Vector
from .vector_math import VectorMath as VM


@dataclass(frozen=True)
class PenStroke:
    start: PenNib
    end: PenNib

    def geometry(self, start: Vector, scale: float, before: Strokeable, after: Strokeable, geom_set: GeometrySet):
        from .stroke import Stroke
        dpl = VM.distance_point_to_line

        def add_start_and_scale(pt: Vector) -> Vector:
            return Stroke.add_start_and_scale(pt, start, scale)

        add_start = before is None or before.stroke_type != StrokeType.Block
        add_end = after is None or after.stroke_type != StrokeType.Block

        outline = geom_set.get_current_outline()

        if add_start:
            if dpl(self.start.pos, self.end.pos, self.start.br) > dpl(self.start.pos, self.end.pos, self.start.tr):
                outline.append(add_start_and_scale(self.start.br))

            outline.append(add_start_and_scale(self.start.tr))

            outline.append(add_start_and_scale(self.start.tl))

            if dpl(self.start.pos, self.end.pos, self.start.bl) > dpl(self.start.pos, self.end.pos, self.start.tl):
                outline.append(add_start_and_scale(self.start.bl))

        if dpl(self.start.pos, self.end.pos, self.end.tl) > dpl(self.start.pos, self.end.pos, self.end.bl):
            outline.append(add_start_and_scale(self.end.tl))

        outline.append(add_start_and_scale(self.end.bl))
        outline = [add_start_and_scale(self.end.br)] + outline

        if dpl(self.start.pos, self.end.pos, self.end.tr) > dpl(self.start.pos, self.end.pos, self.end.br):
            outline = [add_start_and_scale(self.end.tr)] + outline

        geom_set.replace_current_outline(outline)

        if add_end:
            geom_set.add_new_outline()
            geom_set.add_new_hole()
