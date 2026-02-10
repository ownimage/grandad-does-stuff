import math
from shapely.geometry import Point

from .compound_stroke import CompoundStroke
from .font_parameters import FontParameters
from .stroke import Stroke
from .mark import Mark
from .glyph import Glyph
from .stroke_type import StrokeType


class Blackletter:
    def __init__(self, fp: FontParameters):
        self.fp = fp

        # calculated values
        m = fp.pen_thickness / (2 * math.sqrt(2))
        m2 = 2 * m
        m3 = 3 * m
        m4 = 4 * m
        m5 = 5 * m
        m6 = 6 * m
        m7 = 7 * m
        m8 = 8 * m
        m9 = 9 * m

        am_m = fp.ascender - m
        am_3m = fp.ascender - m3
        am_7m = fp.ascender - m7

        xp_m = fp.x_height + m
        xm_m = fp.x_height - m
        xm_2m = fp.x_height - m2
        xm_3m = fp.x_height - m3
        xm_4m = fp.x_height - m4
        xm_7m = fp.x_height - m7

        bp_m = fp.baseline + m
        bp_2m = fp.baseline + m2
        bp_3m = fp.baseline + m3

        dp_3m = fp.descender + m3

        # flourishes
        f_dot = Stroke(Point(m2, -m2))

        f_f_footer = CompoundStroke([
            Stroke(Point(-m4, 0), StrokeType.Move),
            f_dot
        ])

        f_i_footer = CompoundStroke([
            Stroke(Point(0, m), StrokeType.Extend),
            Stroke(Point(-m, m), StrokeType.Move),
            f_dot
        ])

        # strokes
        s_a1 = Stroke(Point(0, bp_3m - xm_3m))

        s_b1 = Stroke(Point(0, bp_3m - am_m))

        s_c1 = Stroke(Point(m2, m2))

        s_d1 = Stroke(Point(m4, -m4))

        s_f1 = Stroke(Point(0, dp_3m - am_3m))
        s_f2 = Stroke(Point(m6, 0))

        s_g1 = Stroke(Point(0, dp_3m - xm_3m))

        s_h1 = Stroke(Point(0, 0 - (fp.ascender - m2)))

        s_i1 = Stroke(Point(0, m - xm_m))

        s_j1 = Stroke(Point(0, dp_3m - xm_m))

        s_k1 = Stroke(Point(m4, 0))
        s_k2 = Stroke(Point(0, 10 * m - fp.x_height))

        s_l1 = Stroke(Point(0, m2 - (fp.ascender - m2)))

        s_m2 = Stroke(Point(0, -xm_4m))

        # compound strokes
        cs_a1 = CompoundStroke([s_a1, f_dot])
        cs_a2 = CompoundStroke([f_dot, s_a1, f_dot])

        cs_b1 = CompoundStroke([s_b1, f_dot])
        cs_b2 = CompoundStroke([f_dot, s_a1])

        cs_c1 = CompoundStroke([s_a1, f_dot, s_c1])

        cs_g1 = CompoundStroke([f_dot, s_g1])

        cs_k1 = CompoundStroke([s_k1, s_k2, f_dot])

        cs_a2 = CompoundStroke([f_dot, s_a1, f_dot])

        cs_m2 = CompoundStroke([f_dot, s_m2]).add_after(f_i_footer)

        # marks
        m_a1 = Mark(Point(0, xm_3m), cs_a1)
        m_a2 = Mark(Point(m2, xm_m), cs_a2)

        m_b1 = Mark(Point(0, am_m), cs_b1)
        m_b2 = Mark(Point(m2, xm_m), cs_b2)

        m_c1 = Mark(Point(0, xm_3m), cs_c1)
        m_c2 = Mark(Point(m2, xm_m), f_dot)

        m_d1 = Mark(Point(0, xp_m, 0), [s_d1, s_a1])

        m_e1 = Mark(Point(0, xm_7m), s_c1)

        m_f1 = Mark(Point(0, am_3m), CompoundStroke(s_f1).add_after(f_f_footer))
        m_f2 = Mark(Point(m2, am_m), f_dot)
        m_f3 = Mark(Point(-m3, fp.tbar), s_f2)

        m_g1 = Mark(Point(m2, xm_m), cs_g1.add_after(f_f_footer))

        m_h1 = Mark(Point(0, fp.ascender - m), CompoundStroke(s_h1).add_after(f_i_footer))

        m_i1 = Mark(Point(0, fp.x_height - m), CompoundStroke(s_i1).add_after(f_i_footer))
        m_i_dot = Mark(Point(-m, fp.tbar), f_dot)

        m_j1 = Mark(Point(0, xm_m), CompoundStroke(s_j1).add_after(f_f_footer))

        m_k1 = Mark(Point(0, fp.x_height - 7 * m), cs_k1)

        m_l1 = Mark(Point(0, fp.ascender - m), CompoundStroke([s_l1, f_dot]))

        m_m2 = Mark(Point(m2, fp.x_height - m), cs_m2)
        m_m3 = m_a2.plus(Point(m4, 0))

        # glyphs
        default_width = 8 * m
        self.glyph_map = {
            'a': Glyph(Point(0, 0), [m_a1, m_a2], default_width),
            'b': Glyph(Point(0, 0), [m_b1, m_b2], default_width),
            'c': Glyph(Point(0, 0), [m_c1, m_c2], m6),
            'd': Glyph(Point(0, 0), [m_a1, m_d1], default_width),
            'e': Glyph(Point(0, 0), [m_c1, m_c2, m_e1], default_width),
            'f': Glyph(Point(0, 0), [m_f1, m_f2, m_f3], m4),
            'g': Glyph(Point(0, 0), [m_a1, m_g1], default_width),
            'h': Glyph(Point(0, 0), [m_h1, m_a2], m9),
            'i': Glyph(Point(0, 0), [m_i1, m_i_dot], m4),
            'j': Glyph(Point(0, 0), [m_j1, m_i_dot], m4),
            'k': Glyph(Point(0, 0), [m_h1, m_c2, m_e1, m_k1], m9),
            'l': Glyph(Point(0, 0), [m_l1], m5),
            'm': Glyph(Point(0, 0), [m_i1, m_m2, m_m3], 13 * m),
            'n': Glyph(Point(0, 0), [m_i1, m_a2], default_width),
        }

    def svg(self, posn: Point, chars: str, scale: float):
        svg = ""
        start = posn
        for c in chars:
            g = self.glyph_map[c]
            svg += f"<!-- char {c} -->\n"
            svg += g.svg(start, self.fp, scale)
            w = g.width
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
