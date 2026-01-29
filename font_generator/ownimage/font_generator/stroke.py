import math
from enum import Enum
from vector2d import Vector2D


class StrokeType(Enum):
    Block = 1
    Line = 2


class Stroke:
    def __init__(self, vec: Vector2D, stroke_type: StrokeType):
        self.vec = vec
        self.stroke_type = stroke_type

    def svg(self, start: Vector2D, scale: float):
        x1 = start.x * scale
        y1 = start.y * scale
        x2 = (start.x + self.vec.x) * scale
        y2 = (start.y + self.vec.y) * scale
        svg = f"""<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="2" />\n"""
        return start.__add__(self.vec), svg

    def svg2(self, start: Vector2D, scale: float, pen_thickness: float):
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
