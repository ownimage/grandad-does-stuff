import math
from enum import Enum
from shapely.geometry import Point

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

        fill_attr = 'fill="black"' if fp.filled else 'fill="none"'
        svg = f"""
        <path d ="M{p1.x} {p1.y} L{p2.x} {p2.y} L{p3.x} {p3.y} L{p4.x} {p4.y} Z" {fill_attr} stroke="black" stroke-width="2" />
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
