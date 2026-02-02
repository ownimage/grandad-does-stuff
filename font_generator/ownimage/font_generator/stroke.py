import math
from enum import Enum
from vector2d import Vector2D

from .strokeable import Strokeable


class StrokeType(Enum):
    Block = 1
    Line = 2


class Stroke(Strokeable):
    def __init__(self, vec: Vector2D, stroke_type: StrokeType):
        super().__init__()
        self.vec = vec
        self.stroke_type = stroke_type

    def svg(self, start: Vector2D, scale: float, pen_thickness: float):
        d = scale * pen_thickness / (2 * math.sqrt(2))
        s = Vector2D(-d, -d)
        s2 = s.__mul__(2)
        v = self.vec.__mul__(scale)

        p1 = start.__mul__(scale).__add__(s)
        p2 = p1.__add__(v)
        p3 = p2.__sub__(s2)
        p4 = p3.__sub__(v)

        svg = f"""
        <line x1="{p1.x}" y1="{p1.y}" x2="{p2.x}" y2="{p2.y}" stroke="black" stroke-width="2" />
        <line x1="{p2.x}" y1="{p2.y}" x2="{p3.x}" y2="{p3.y}" stroke="black" stroke-width="2" />
        <line x1="{p3.x}" y1="{p3.y}" x2="{p4.x}" y2="{p4.y}" stroke="black" stroke-width="2" />
        <line x1="{p4.x}" y1="{p4.y}" x2="{p1.x}" y2="{p1.y}" stroke="black" stroke-width="2" />
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

        paths = [f"S {p1.x:.5f},{p1.y:.5f} L {p2.x:.5f},{p2.y:.5f} L {p3.x:.5f},{p3.y:.5f} L {p4.x:.5f},{p4.y:.5f} L {p1.x:.5f},{p1.y:.5f}"]
        return start.__add__(self.vec), paths
