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
        m = fp.pen_thickness / (2 * math.sqrt(2))

        am_m = fp.ascender - m
        am_3m = fp.ascender - 3 * m
        am_7m = fp.ascender - 7 * m

        xp_m = fp.x_height + m
        xm_m = fp.x_height - m
        xm_3m = fp.x_height - 3 * m
        xm_7m = fp.x_height - 7 * m

        bp_m = fp.baseline + m
        bp_2m = fp.baseline + 2 * m
        bp_3m = fp.baseline + 3 * m

        dp_3m = fp.descender + 3 * m

        # strokes
        s_a1 = Stroke(Point(0, bp_3m - xm_3m), StrokeType.Block)
        s_a2 = Stroke(Point(2 * m, -2 * m), StrokeType.Block)

        s_b1 = Stroke(Point(0, bp_3m - am_m), StrokeType.Block)

        s_c1 = Stroke(Point(2 * m, 2 * m), StrokeType.Block)

        s_d1 = Stroke(Point(4 * m, -4 * m), StrokeType.Block)

        s_f1 = Stroke(Point(0, 3 * m - fp.descender - fp.ascender), StrokeType.Block)
        s_f2 = Stroke(Point(6 * m, 0), StrokeType.Block)

        s_g1 = Stroke(Point(0, 3 * m - fp.x_height - fp.descender), StrokeType.Block)

        # compound strokes
        cs_a1 = CompoundStroke([s_a1, s_a2])
        cs_a2 = CompoundStroke([s_a2, s_a1, s_a2])

        cs_b1 = CompoundStroke([s_b1, s_a2])
        cs_b2 = CompoundStroke([s_a2, s_a1])

        cs_c1 = CompoundStroke([s_a1, s_a2, s_c1])

        cs_g1 = CompoundStroke([s_a2, s_g1])

        # marks
        m_a1 = Mark(Point(0, xm_3m), [cs_a1])
        m_a2 = Mark(Point(2 * m, xm_m), [cs_a2])

        m_b1 = Mark(Point(0, am_m), [cs_b1])
        m_b2 = Mark(Point(2 * m, xm_m), [cs_b2])

        m_c1 = Mark(Point(0, xm_3m), [cs_c1])
        m_c2 = Mark(Point(2 * m, xm_m), [s_a2])

        m_d1 = Mark(Point(0, xp_m, 0), [s_d1, s_a1])

        m_e1 = Mark(Point(0, xm_7m), [s_c1])

        m_f1 = Mark(Point(0, am_3m), [s_f1])
        m_f2 = Mark(Point(-4 * m, -fp.descender), [s_a2])
        m_f3 = Mark(Point(2 * m, am_m), [s_a2])
        m_f4 = Mark(Point(-3 * m, am_7m), [s_f2])

        m_g1 = Mark(Point(2 * m, xm_m), [cs_g1])
        m_g2 = Mark(Point(0, -fp.descender), [s_a2])

        # glyphs
        g_a1 = Glyph(Point(0, 0), [m_a1, m_a2])
        g_b1 = Glyph(Point(0, 0), [m_b1, m_b2])
        g_c1 = Glyph(Point(0, 0), [m_c1, m_c2])
        g_d1 = Glyph(Point(0, 0), [m_a1, m_d1])
        g_e1 = Glyph(Point(0, 0), [m_c1, m_c2, m_e1])
        g_f1 = Glyph(Point(0, 0), [m_f1, m_f2, m_f3, m_f4])
        g_g1 = Glyph(Point(0, 0), [m_a1, m_g1, m_g2])

        # glyph map
        self.glyph_map = {'a': g_a1, 'b': g_b1, 'c': g_c1, 'd': g_d1, 'e': g_e1, 'f': g_f1, 'g': g_g1}

        self.glyph_widths = {'default': 8 * m}

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
        return g.birdfont_path(self.fp, scale)

    def glyph_keys(self):
        return self.glyph_map.keys()
