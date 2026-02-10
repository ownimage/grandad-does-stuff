from __future__ import annotations

import math

from shapely.geometry import Point, LineString
from shapely.affinity import rotate

from .font_parameters import FontParameters
from .geom import Geom
from .geometry_set import GeometrySet
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector_math import VectorMath as VM


class Stroke(Strokeable):


    def __init__(self, vec: Point, stroke_type: StrokeType = StrokeType.Block):
        super().__init__(stroke_type)
        self.vec = vec

    @staticmethod
    def from_xy(x: float, y: float, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(Point(x, y), stroke_type)

    @staticmethod
    def between(start: Point, end: Point, stroke_type: StrokeType = StrokeType.Block) -> Stroke:
        return Stroke(VM.subtract_points(start, end), stroke_type)

    def extend(self, e: Stroke) -> Stroke:
        if e.stroke_type != Stroke.StrokeType.Extend:
            raise RuntimeError("Stroke of wrong type.")
        return Stroke(VM.add_points(self.vec, e.vec), self.stroke_type)

    def get_geom(self, start: Point, fp: FontParameters, scale: float, prev: Strokeable, next: Strokeable, geom_set: GeometrySet):
        if self.stroke_type == StrokeType.Move:
            return VM.add_points(start, self.vec)

        d = scale * fp.pen_thickness / (2 * math.sqrt(2))
        s = Point(-d, -d)
        s2 = VM.scale_point(s, 2)
        v = VM.scale_point(self.vec, scale)

        p1 = VM.add_points(VM.scale_point(start, scale), s)
        p2 = VM.add_points(p1, v)
        p3 = VM.subtract_points(p2, s2)
        p4 = VM.subtract_points(p3, v)

        if prev is None or prev.stroke_type != StrokeType.Block:
            geom_set.get_current_outline().extend([p3, p4, p1, p2])
        else:
            curr = geom_set.get_current_outline()
            new = [p3] + curr + [p2]
            geom_set.replace_current_outline(new)

        if next is None or next.stroke_type != StrokeType.Block:
            geom_set.add_new_outline()

        return VM.add_points(start, self.vec)

    def geom(self, start: Point, fp: FontParameters, scale: float) -> tuple[Point, list[Geom]]:

        if self.stroke_type == StrokeType.Move:
            return VM.add_points(start, self.vec), []

        d = scale * fp.pen_thickness / (2 * math.sqrt(2))
        s = Point(-d, -d)
        s2 = VM.scale_point(s, 2)
        v = VM.scale_point(self.vec, scale)

        p1 = VM.add_points(VM.scale_point(start, scale), s)
        p2 = VM.add_points(p1, v)
        p3 = VM.subtract_points(p2, s2)
        p4 = VM.subtract_points(p3, v)

        # inside line 1
        line_thickness = 0.04 * scale
        offset1 = rotate(VM.scale_point(VM.normalize(self.vec), line_thickness), 90, origin=(0, 0))
        offset4 = rotate(VM.scale_point(VM.normalize(VM.subtract_points(p1, p4)), line_thickness), 90, origin=(0, 0))

        p1offset1 = VM.add_points(p1, offset1)
        p2offset1 = VM.add_points(p2, offset1)
        p2offset2 = VM.subtract_points(p2, offset4)
        p3offset2 = VM.subtract_points(p3, offset4)
        p3offset3 = VM.subtract_points(p3, offset1)
        p4offset3 = VM.subtract_points(p4, offset1)
        p4offset4 = VM.add_points(p4, offset4)
        p1offset4 = VM.add_points(p1, offset4)

        insideLine1 = LineString([p1offset1, p2offset1])
        insideLine2 = LineString([p2offset2, p3offset2])
        insideLine3 = LineString([p3offset3, p4offset3])
        insideLine4 = LineString([p4offset4, p1offset4])

        ip1 = insideLine4.intersection(insideLine1)
        ip2 = insideLine1.intersection(insideLine2)
        ip3 = insideLine2.intersection(insideLine3)
        ip4 = insideLine3.intersection(insideLine4)

        geom = [Geom([p1, p2, p3, p4])]

        if ip1.is_empty or ip2.is_empty or ip3.is_empty or ip4.is_empty:
            p1offset = VM.subtract_points(p1, offset4)
            p3offset = VM.subtract_points(p3, offset4)
            if fp.filled:
                geom += [Geom([p1, p1offset, p3offset, p3])]
            return VM.add_points(start, self.vec), geom

        if not fp.filled:
            geom += [Geom([ip1, ip2, ip3, ip4], Geom.GeomType.White)]
        return VM.add_points(start, self.vec), geom

    def svg(self, start: Point, fp: FontParameters, scale: float):
        end, geoms = self.geom(start, fp, scale)
        svg = list(map(self.geom_to_svg, geoms))
        return end, "\n".join(svg)

    def geom_to_svg(self, geom) -> str:
        colour = "black" if geom.geom_type == Geom.GeomType.Black else "white"
        p0 = geom.points[0]
        svg = f"""<path d ="M{p0.x} {p0.y} """
        for p in geom.points[1:]:
            svg += f"""L{p.x} {p.y} """
        svg += f"""Z" fill="{colour}" stroke="black" stroke-width=".5" />\n"""
        return svg

    def birdfont_path(self, start: Point, fp: FontParameters, scale: float):
        end, geoms = self.geom(start, fp, scale)
        paths = list(map(self.geom_to_path, geoms))
        return end, paths

    def geom_to_path(self, geom):
        points = geom.points if geom.geom_type == Geom.GeomType.Black else geom.points[::-1]
        p0 = points[0]
        data = f"""S {p0.x:.5f},{p0.y:.5f} """
        for p in points[1:]:
            data += f"""L {p.x:.5f},{p.y:.5f} """
        path = {"data": data}
        return path
