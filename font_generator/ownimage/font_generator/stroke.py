import math
from enum import Enum
from vector2d import Vector2D

from .font_parameters import FontParameters
from .strokeable import Strokeable


class StrokeType(Enum):
    Block = 1
    Line = 2


class Stroke(Strokeable):
    def __init__(self, vec: Vector2D, stroke_type: StrokeType):
        super().__init__()
        self.vec = vec
        self.stroke_type = stroke_type

    def svg(self, start: Vector2D, fp: FontParameters, scale: float):
        d = scale * fp.pen_thickness / (2 * math.sqrt(2))
        s = Vector2D(-d, -d)
        s2 = s.__mul__(2)
        v = self.vec.__mul__(scale)

        p1 = start.__mul__(scale).__add__(s)
        p2 = p1.__add__(v)
        p3 = p2.__sub__(s2)
        p4 = p3.__sub__(v)

        fill_attr = 'fill="black"' if fp.filled else 'fill="none"'
        svg = f"""
        <path d ="M{p1.x} {p1.y} L{p2.x} {p2.y} L{p3.x} {p3.y} L{p4.x} {p4.y} Z" {fill_attr} stroke="black" stroke-width="2" />
                """
        return start.__add__(self.vec), svg

    def birdfont_path(self, start: Vector2D, scale: float, pen_thickness: float):
        d = scale * pen_thickness / (2 * math.sqrt(2))
        s = Vector2D(-d, -d)
        s2 = s.__mul__(2)
        v = self.vec.__mul__(scale)

        p1 = start.__mul__(scale).__add__(s)
        p2 = p1.__add__(v)
        p3 = p2.__sub__(s2)
        p4 = p3.__sub__(v)

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
        return start.__add__(self.vec), paths
