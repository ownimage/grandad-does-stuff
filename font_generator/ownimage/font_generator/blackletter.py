import math
from shapely.geometry import Point

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

        self.xp_m = fp.x_height +  self.m
        self.xm_m = fp.x_height - self.m
        self.xm_3m = fp.x_height - 3 * self.m
        self.xm_7m = fp.x_height - 7 * self.m

        self.bp_3m = fp.baseline + 3 * self.m

        # strokes
        self.s_a1 = Stroke(Point(0, self.bp_3m - self.xm_3m), StrokeType.Block)
        self.s_a2 = Stroke(Point(2 * self.m, -2 * self.m), StrokeType.Block)

        self.s_b1 = Stroke(Point(0, self.bp_3m - fp.ascender), StrokeType.Block)

        self.s_c1 = Stroke(Point(2 * self.m, 2 * self.m), StrokeType.Block)

        self.s_d1 = Stroke(Point(4 * self.m, -4 * self.m), StrokeType.Block)

        # compound strokes
        self.cs_a1 = CompoundStroke([self.s_a1, self.s_a2])
        self.cs_a2 = CompoundStroke([self.s_a2, self.s_a1, self.s_a2])

        self.cs_b1 = CompoundStroke([self.s_b1, self.s_a2])
        self.cs_b2 = CompoundStroke([self.s_a2, self.s_a1])

        self.cs_c1 = CompoundStroke([self.s_a1, self.s_a2, self.s_c1])

        # marks
        self.m_a1 = Mark(Point(0, self.xm_3m), [self.cs_a1])
        self.m_a2 = Mark(Point(2 * self.m, self.xm_m), [self.cs_a2])

        self.m_b1 = Mark(Point(0, self.fp.ascender), [self.cs_b1])
        self.m_b2 = Mark(Point(2 * self.m, self.xm_m), [self.cs_b2])

        self.m_c1 = Mark(Point(0, self.xm_3m), [self.cs_c1])
        self.m_c2 = Mark(Point(2 * self.m, self.xm_m), [self.s_a2])

        self.m_d1 = Mark(Point(0, self.xp_m, 0), [self.s_d1, self.s_a1])

        self.m_e1 = Mark(Point(0, self.xm_7m), [self.s_c1])

        # glyphs
        self.g_a1 = Glyph(Point(0, 0), [self.m_a1, self.m_a2])
        self.g_b1 = Glyph(Point(0, 0), [self.m_b1, self.m_b2])
        self.g_c1 = Glyph(Point(0, 0), [self.m_c1, self.m_c2])
        self.g_d1 = Glyph(Point(0, 0), [self.m_a1, self.m_d1])
        self.g_e1 = Glyph(Point(0, 0), [self.m_c1, self.m_c2, self.m_e1])

        # glyph map
        self.glyph_map = {'a': self.g_a1, 'b': self.g_b1, 'c': self.g_c1, 'd': self.g_d1, 'e': self.g_e1}

        self.glyph_widths = {'default': 8 * self.m}

    def svg(self, posn: Point, chars: str, scale: float):
        svg = ""
        start = posn
        for c in chars:
            svg += f"<!-- char {c} -->\n"
            svg += self.glyph_map[c].svg(start, self.fp, scale)
            w = self.glyph_widths.get(c, self.glyph_widths['default'])
            start = Point(start.x + w, start.y)
        print(f"svg={svg}")
        return svg

    def svg_known(self, posn: Point, scale: float):
        chars = ''.join(self.glyph_map.keys())
        return self.svg(posn, chars, scale)

    def birdfont_path(self, key, scale: float):
        g = self.glyph_map[key]
        return g.birdfont_path(scale, self.fp.pen_thickness)
