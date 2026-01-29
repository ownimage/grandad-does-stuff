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
