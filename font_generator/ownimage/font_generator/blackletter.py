import math
from vector2d import Vector2D

from .compound_stroke import CompoundStroke
from .font_parameters import FontParameters
from .stroke import Stroke, StrokeType
from .mark import Mark
from .glyph import Glyph


class Blackletter:
    def __init__(self, fp: FontParameters):

        self.fp = fp

        # calculated values
        self.m = fp.pen_thickness / (2 * math.sqrt(2))
        self.xm = fp.x_height - self.m
        self.x3m = fp.x_height - 3 * self.m
        self.b3m = fp.baseline + 3 * self.m

        # strokes
        self.s_a1 = Stroke(Vector2D(0, self.b3m - self.x3m), StrokeType.Block)
        self.s_a2 = Stroke(Vector2D(2 * self.m, -2 * self.m), StrokeType.Block)

        self.s_b1 = Stroke(Vector2D(0, self.b3m - fp.ascender), StrokeType.Block)

        self.s_c1 = Stroke(Vector2D(2 * self.m, 2 * self.m), StrokeType.Block)

        # compound strokes
        self.cs_a1 = CompoundStroke([self.s_a1, self.s_a2])
        self.cs_a2 = CompoundStroke([self.s_a2, self.s_a1, self.s_a2])

        self.cs_b1 = CompoundStroke([self.s_b1, self.s_a2])
        self.cs_b2 = CompoundStroke([self.s_a2, self.s_a1])

        self.cs_c1 = CompoundStroke([self.s_a1, self.s_a2, self.s_c1])

        # marks
        self.m_a1 = Mark(Vector2D(0, self.x3m), [self.cs_a1])
        self.m_a2 = Mark(Vector2D(2 * self.m, self.xm), [self.cs_a2])

        self.m_b1 = Mark(Vector2D(0, self.fp.ascender), [self.cs_b1])
        self.m_b2 = Mark(Vector2D(2 * self.m, self.xm), [self.cs_b2])

        self.m_c1 = Mark(Vector2D(0, self.x3m), [self.cs_c1])
        self.m_c2 = Mark(Vector2D(2 * self.m, self.xm), [self.s_a2])

        # glyphs
        self.g_a1 = Glyph(Vector2D(0, 0), [self.m_a1, self.m_a2])
        self.g_b1 = Glyph(Vector2D(0, 0), [self.m_b1, self.m_b2])
        self.g_c1 = Glyph(Vector2D(0, 0), [self.m_c1, self.m_c2])

        # glyph map
        self.glyph_map = {'a': self.g_a1, 'b': self.g_b1, 'c': self.g_c1}

        self.glyph_widths = {'a': 8 * self.m, 'b': 8 * self.m, 'c': 8 * self.m}

    def svg(self, posn: Vector2D, chars: str, scale: float):
        svg = ""
        start = posn
        for c in chars:
            svg += f"<!-- char {c} -->\n"
            svg += self.glyph_map[c].svg(start, self.fp, scale)
            start += Vector2D(self.glyph_widths[c], 0)
        print(f"svg={svg}")
        return svg

    def birdfont_path(self, key, scale: float):
        g = self.glyph_map[key]
        return g.birdfont_path(scale, self.fp.pen_thickness)
