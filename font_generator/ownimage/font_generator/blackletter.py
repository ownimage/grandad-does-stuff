import math
from vector2d import Vector2D

from ownimage.font_generator.stroke import Stroke, StrokeType
from ownimage.font_generator.mark import Mark
from ownimage.font_generator.glyph import Glyph


class Blackletter:
    def __init__(self, pen_thickness: float, b: float, x: float):
        self.pen_thickness = pen_thickness
        self.b = b
        self.x = x

        self.m = pen_thickness / (2 * math.sqrt(2))
        self.xm = x - self.m
        self.x3m = x - 3 * self.m
        self.b3m = b + 3 * self.m

        self.s_a1 = Stroke(Vector2D(0, self.b3m - self.x3m), StrokeType.Block)
        self.s_a2 = Stroke(Vector2D(2 * self.m, -2 * self.m), StrokeType.Block)

        self.m_a1 = Mark(Vector2D(0, self.x3m), [self.s_a1, self.s_a2])
        self.m_a2 = Mark(Vector2D(2 * self.m, self.xm), [self.s_a2, self.s_a1, self.s_a2])

        self.g_a1 = Glyph(Vector2D(0, 0), [self.m_a1, self.m_a2])

    def svg(self, posn: Vector2D, scale: float):
        return self.g_a1.svg(posn, scale, self.pen_thickness)
