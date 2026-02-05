import math
from enum import Enum
from shapely.geometry import Point, LineString
from shapely.affinity import rotate

from .font_parameters import FontParameters
from .strokeable import Strokeable
from .vector_math import VectorMath as VM



class StrokeType(Enum):
    Block = 1
    Line = 2


class Stroke(Strokeable):
    def __init__(self, vec: Point, stroke_type: StrokeType):
        super().__init__()
        self.vec = vec
        self.stroke_type = stroke_type

    def svg(self, start: Point, fp: FontParameters, scale: float):
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

        fill_attr = 'fill="black"' if fp.filled else 'fill="none"'

        if ip1.is_empty or ip2.is_empty or ip3.is_empty or ip4.is_empty:
            p1offset = VM.subtract_points(p1, offset4)
            p3offset = VM.subtract_points(p3, offset4)
            svg = f"""
            <path d ="M{p1.x} {p1.y} L{p1offset.x} {p1offset.y} L{p3offset.x} {p3offset.y} L{p3.x} {p3.y} Z" {fill_attr} stroke="black" stroke-width=".5" />
                    """
            return VM.add_points(start, self.vec), svg

        svg = f"""
        <path d ="M{p1.x} {p1.y} L{p2.x} {p2.y} L{p3.x} {p3.y} L{p4.x} {p4.y} Z" {fill_attr} stroke="black" stroke-width=".5" />
        <path d ="M{ip1.x} {ip1.y} L{ip2.x} {ip2.y} L{ip3.x} {ip3.y} L{ip4.x} {ip4.y} Z" {fill_attr} stroke="black" stroke-width=".5" />
                """
        return VM.add_points(start, self.vec), svg

    def birdfont_path(self, start: Point, scale: float, pen_thickness: float):
        d = scale * pen_thickness / (2 * math.sqrt(2))
        s = Point(-d, -d)
        s2 = VM.scale_point(s, 2)
        v = VM.scale_point(self.vec, scale)

        p1 = VM.add_points(VM.scale_point(start, scale), s)
        p2 = VM.add_points(p1, v)
        p3 = VM.subtract_points(p2, s2)
        p4 = VM.subtract_points(p3, v)

        paths = [
            {
                "data": f"S {p1.x:.5f},{p1.y:.5f} L {p2.x:.5f},{p2.y:.5f} L {p3.x:.5f},{p3.y:.5f} L {p4.x:.5f},{p4.y:.5f} L {p1.x:.5f},{p1.y:.5f}",
                "stroke": ".1"
            },
            # {
            #     "data": f"S {p1.x:.5f},{p1.y:.5f} L {p2.x:.5f},{p2.y:.5f} L {p3.x:.5f},{p3.y:.5f} L {p4.x:.5f},{p4.y:.5f} L {p1.x:.5f},{p1.y:.5f}",
            #     "fill": "black",
            # }
        ]
        return VM.add_points(start, self.vec), paths
