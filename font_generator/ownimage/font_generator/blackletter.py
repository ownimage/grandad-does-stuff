import math
from vector2d import Vector2D

from .stroke import Stroke, StrokeType
from .mark import Mark
from .glyph import Glyph


class Blackletter:
    def __init__(self, pen_thickness: float, b: float, x: float, a: float):
        self.pen_thickness = pen_thickness
        self.b = b
        self.x = x
        self.a = a

        # calculated values
        self.m = pen_thickness / (2 * math.sqrt(2))
        self.xm = x - self.m
        self.x3m = x - 3 * self.m
        self.b3m = b + 3 * self.m

        # strokes
        self.s_a1 = Stroke(Vector2D(0, self.b3m - self.x3m), StrokeType.Block)
        self.s_a2 = Stroke(Vector2D(2 * self.m, -2 * self.m), StrokeType.Block)

        self.s_b1 = Stroke(Vector2D(0, self.b3m - self.a), StrokeType.Block)

        # marks
        self.m_a1 = Mark(Vector2D(0, self.x3m), [self.s_a1, self.s_a2])
        self.m_a2 = Mark(Vector2D(2 * self.m, self.xm), [self.s_a2, self.s_a1, self.s_a2])

        self.m_b1 = Mark(Vector2D(0, self.a), [self.s_b1, self.s_a2])
        self.m_b2 = Mark(Vector2D(2 * self.m, self.xm), [self.s_a2, self.s_a1])

        # glyphs
        self.g_a1 = Glyph(Vector2D(0, 0), [self.m_a1, self.m_a2])
        self.g_b1 = Glyph(Vector2D(0, 0), [self.m_b1, self.m_b2])

        # glyph map
        self.glyph_map = {'a': self.g_a1, 'b': self.g_b1}

        self.glyph_widths = {'a': 8 * self.m, 'b': 8 * self.m}

    def svg(self, posn: Vector2D, chars: str, scale: float):
        svg = ""
        start = posn
        for c in chars:
            svg += self.glyph_map[c].svg(start, scale, self.pen_thickness)
            start += Vector2D(self.glyph_widths[c], 0)
        return svg

    def birdfont_path(self, key, scale: float):
        g = self.glyph_map[key]
        return g.birdfont_path(scale, self.pen_thickness)
