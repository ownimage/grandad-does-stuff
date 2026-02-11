from __future__ import annotations

import math

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector import Vector
from .vector_math import VectorMath as VM


class Stroke(Strokeable):

    def __init__(self, vec: Vector, stroke_type: StrokeType = StrokeType.Block):
        super().__init__(stroke_type)
        self.vec = vec

    @staticmethod
    def from_xy(x: float, y: float, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(Vector(x, y), stroke_type)

    @staticmethod
    def between(start: Vector, end: Vector, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(start - end, stroke_type)

    def extend(self, e: Stroke) -> Stroke:
        if e.stroke_type != Stroke.StrokeType.Extend:
            raise RuntimeError("Stroke of wrong type.")
        return Stroke(self.vec + e.vec, self.stroke_type)

    def get_geom(self, start: Vector, fp: FontParameters, scale: float, prev: Strokeable, next: Strokeable, geom_set: GeometrySet):
        if self.stroke_type == StrokeType.Move:
            return start + self.vec

        offset = fp.line_thickness * fp.pen_thickness * scale / 2
        sqrt2 = math.sqrt(2)
        d = scale * fp.pen_thickness / (2 * sqrt2)
        s = Vector(-d, -d)
        s2 = 2 * s
        v = self.vec * scale

        p1 = (start * scale) + s
        p2 = p1 + v
        p3 = p2 - s2
        p4 = p3 - v

        ip1 = VM.offset_intersection(p1, self.vec, s, offset)
        ip2 = VM.offset_intersection(p2, s * -1, self.vec, offset)
        ip3 = VM.offset_intersection(p3, -1 * self.vec, -1 * s, offset)
        ip4 = VM.offset_intersection(p4, -1 * self.vec, s, offset)

        if next is not None and next.stroke_type == StrokeType.Block:
            p = VM.offset_intersection(p2, self.vec, next.vec, offset)
            ip2 = p if p is not None else ip2

            p = VM.offset_intersection(p3, self.vec, next.vec, -offset)
            ip3 = p if p is not None else ip3

        if prev is None or prev.stroke_type != StrokeType.Block:
            geom_set.get_current_outline().extend([p3, p4, p1, p2])
            geom_set.get_current_hole().extend([ip3, ip4, ip1, ip2])
        else:
            outline = geom_set.get_current_outline()
            new_outline = [p3] + outline + [p2]
            geom_set.replace_current_outline(new_outline)

            hole = geom_set.get_current_hole()
            new_hole = [ip3] + hole + [ip2]
            geom_set.replace_current_hole(new_hole)

        if next is None or next.stroke_type != StrokeType.Block:
            geom_set.add_new_outline()
            geom_set.add_new_hole()

        return start + self.vec

        # # def geom(self, start: Vector, fp: FontParameters, scale: float) -> tuple[Vector, list[Geom]]:
        # #
        # #     if self.stroke_type == StrokeType.Move:
        # #         return VM.add_points(start, self.vec), []
        # #
        # #     d = scale * fp.pen_thickness / (2 * math.sqrt(2))
        # #     s = Vector(-d, -d)
        # #     s2 = VM.scale_point(s, 2)
        # #     v = VM.scale_point(self.vec, scale)
        # #
        # #     p1 = VM.add_points(VM.scale_point(start, scale), s)
        # #     p2 = VM.add_points(p1, v)
        # #     p3 = VM.subtract_points(p2, s2)
        # #     p4 = VM.subtract_points(p3, v)
        # #
        # #     # inside line 1
        # #     line_thickness = 0.04 * scale
        # #     offset1 = rotate(VM.scale_point(VM.normalize(self.vec), line_thickness), 90, origin=(0, 0))
        # #     offset4 = rotate(VM.scale_point(VM.normalize(VM.subtract_points(p1, p4)), line_thickness), 90, origin=(0, 0))
        # #
        # #     p1offset1 = VM.add_points(p1, offset1)
        # #     p2offset1 = VM.add_points(p2, offset1)
        # #     p2offset2 = VM.subtract_points(p2, offset4)
        # #     p3offset2 = VM.subtract_points(p3, offset4)
        # #     p3offset3 = VM.subtract_points(p3, offset1)
        # #     p4offset3 = VM.subtract_points(p4, offset1)
        # #     p4offset4 = VM.add_points(p4, offset4)
        # #     p1offset4 = VM.add_points(p1, offset4)
        # #
        # #     insideLine1 = LineString([p1offset1, p2offset1])
        # #     insideLine2 = LineString([p2offset2, p3offset2])
        # #     insideLine3 = LineString([p3offset3, p4offset3])
        # #     insideLine4 = LineString([p4offset4, p1offset4])
        # #
        # #     ip1 = insideLine4.intersection(insideLine1)
        # #     ip2 = insideLine1.intersection(insideLine2)
        # #     ip3 = insideLine2.intersection(insideLine3)
        # #     ip4 = insideLine3.intersection(insideLine4)
        # #
        # #     geom = [Geom([p1, p2, p3, p4])]
        # #
        # #     if ip1.is_empty or ip2.is_empty or ip3.is_empty or ip4.is_empty:
        # #         p1offset = VM.subtract_points(p1, offset4)
        # #         p3offset = VM.subtract_points(p3, offset4)
        # #         if fp.filled:
        # #             geom += [Geom([p1, p1offset, p3offset, p3])]
        # #         return VM.add_points(start, self.vec), geom
        # #
        # #     if not fp.filled:
        # #         geom += [Geom([ip1, ip2, ip3, ip4], Geom.GeomType.White)]
        # #     return VM.add_points(start, self.vec), geom
        # #
        # # def svg(self, start: Vector, fp: FontParameters, scale: float):
        # #     end, geoms = self.geom(start, fp, scale)
        # #     svg = list(map(self.geom_to_svg, geoms))
        # #     return end, "\n".join(svg)
        # #
        # # def geom_to_svg(self, geom) -> str:
        # #     colour = "black" if geom.geom_type == Geom.GeomType.Black else "white"
        # #     p0 = geom.points[0]
        # #     svg = f"""<path d ="M{p0.x} {p0.y} """
        # #     for p in geom.points[1:]:
        # #         svg += f"""L{p.x} {p.y} """
        # #     svg += f"""Z" fill="{colour}" stroke="black" stroke-width=".5" />\n"""
        # #     return svg
        #
        # def birdfont_path(self, start: Vector, fp: FontParameters, scale: float):
        #     end, geoms = self.geom(start, fp, scale)
        #     paths = list(map(self.geom_to_path, geoms))
        #     return end, paths
        #
        # def geom_to_path(self, geom):
        #     points = geom.points if geom.geom_type == Geom.GeomType.Black else geom.points[::-1]
        #     p0 = points[0]
        #     data = f"""S {p0.x:.5f},{p0.y:.5f} """
        #     for p in points[1:]:
        #         data += f"""L {p.x:.5f},{p.y:.5f} """
        #     path = {"data": data}
        #     return path
