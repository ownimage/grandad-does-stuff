import math

from .compound_stroke import CompoundStroke
from .font_parameters import FontParameters
from .glyph import Glyph
from .mark import Mark
from .stroke import Stroke
from .stroke_line import StrokeLine
from .stroke_type import StrokeType
from .vector import Vector


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
        f_dot = Stroke(Vector(m2, -m2))

        f_f_footer = CompoundStroke([
            Stroke(Vector(-m4, 0), StrokeType.Move),
            f_dot
        ])

        f_i_footer = CompoundStroke([
            Stroke(Vector(0, m), StrokeType.Extend),
            Stroke(Vector(-m, m), StrokeType.Move),
            f_dot
        ])

        # strokes
        s_a1 = Stroke(Vector(0, bp_3m - xm_3m))

        s_b1 = Stroke(Vector(0, bp_3m - am_m))

        s_c1 = CompoundStroke([Stroke(Vector(m, m), StrokeType.Move), StrokeLine(Vector(m2, m2))])

        s_d1 = Stroke(Vector(m4, -m4))

        s_f1 = Stroke(Vector(0, dp_3m - am_3m))
        s_f2 = Stroke(Vector(m6, 0))

        s_g1 = Stroke(Vector(0, dp_3m - xm_3m))

        s_h1 = Stroke(Vector(0, 0 - (fp.ascender - m2)))

        s_i1 = Stroke(Vector(0, m - xm_m))

        s_j1 = Stroke(Vector(0, dp_3m - xm_m))

        s_k1 = Stroke(Vector(m4, 0))
        s_k2 = Stroke(Vector(0, 10 * m - fp.x_height))

        s_l1 = Stroke(Vector(0, m2 - (fp.ascender - m2)))

        s_m2 = Stroke(Vector(0, -xm_4m))

        s_s1 = Stroke.down(m6)
        s_s2 = StrokeLine.right(m4)
        s_s3 = Stroke.down(fp.x_height - 10 * m)

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
        m_a1 = Mark(Vector(0, xm_3m), cs_a1)
        m_a2 = Mark(Vector(m2, xm_m), cs_a2)

        m_b1 = Mark(Vector(0, am_m), cs_b1)
        m_b2 = Mark(Vector(m2, xm_m), cs_b2)

        m_c1 = Mark(Vector(0, xm_3m), cs_c1)
        m_c2 = Mark(Vector(m2, xm_m), f_dot)

        m_d1 = Mark(Vector(0, xp_m), [s_d1, s_a1])

        m_e1 = Mark(Vector(0, xm_7m), s_c1)

        m_f1 = Mark(Vector(0, am_3m), CompoundStroke(s_f1).add_after(f_f_footer))
        m_f2 = Mark(Vector(m2, am_m), f_dot)
        m_f3 = Mark(Vector(-m3, fp.tbar), s_f2)

        m_g1 = Mark(Vector(m2, xm_m), cs_g1.add_after(f_f_footer))

        m_h1 = Mark(Vector(0, fp.ascender - m), CompoundStroke(s_h1).add_after(f_i_footer))

        m_i1 = Mark(Vector(0, fp.x_height - m), CompoundStroke(s_i1).add_after(f_i_footer))
        m_i_dot = Mark(Vector(-m, fp.tbar), f_dot)

        m_j1 = Mark(Vector(0, xm_m), CompoundStroke(s_j1).add_after(f_f_footer))

        m_k1 = Mark(Vector(0, fp.x_height - 7 * m), cs_k1)

        m_l1 = Mark(Vector(0, fp.ascender - m), CompoundStroke([s_l1, f_dot]))

        m_m2 = Mark(Vector(m2, fp.x_height - m), cs_m2)
        m_m3 = m_a2.plus(Vector(m4, 0))

        m_p1 = Mark(Vector(0, xm_m), s_j1)
        m_p3 = Mark(Vector(-m2, m5), Stroke.from_xy(m4, -m4))

        m_s1 = Mark(Vector(0, fp.x_height - m), CompoundStroke([s_s1, s_s2, s_s3]).add_after(f_f_footer))

        # glyphs
        default_width = 8 * m
        self.glyph_map = {
            'a': Glyph(Vector(0, 0), [m_a1, m_a2], default_width),
            'b': Glyph(Vector(0, 0), [m_b1, m_b2], default_width),
            'c': Glyph(Vector(0, 0), [m_c1, m_c2], default_width),
            'd': Glyph(Vector(0, 0), [m_a1, m_d1], default_width),
            'e': Glyph(Vector(0, 0), [m_c1, m_c2, m_e1], default_width),
            'f': Glyph(Vector(0, 0), [m_f1, m_f2, m_f3], m4),
            'g': Glyph(Vector(0, 0), [m_a1, m_g1], default_width),
            'h': Glyph(Vector(0, 0), [m_h1, m_a2], m9),
            'i': Glyph(Vector(0, 0), [m_i1, m_i_dot], m4),
            'j': Glyph(Vector(0, 0), [m_j1, m_i_dot], m4),
            'k': Glyph(Vector(0, 0), [m_h1, m_c2, m_e1, m_k1], m9),
            'l': Glyph(Vector(0, 0), [m_l1], m5),
            'm': Glyph(Vector(0, 0), [m_i1, m_m2, m_m3], 13 * m),
            'n': Glyph(Vector(0, 0), [m_i1, m_a2], default_width),
            'o': Glyph(Vector(0, 0), [m_a1, m_b2], default_width),
            'p': Glyph(Vector(0, 0), [m_p1, m_b2, m_p3], default_width),
            'r': Glyph(Vector(0, 0), [m_i1, m_c2], default_width),
            's': Glyph(Vector(0, 0), [m_s1, m_c2], m4),

        }

    def svg(self, posn: Vector, chars: str, scale: float):
        svg = ""
        start = posn
        for c in chars:
            g = self.glyph_map[c]
            svg += f"<!-- char {c} -->\n"
            svg += g.svg(start, self.fp, scale)
            w = g.width
            start = Vector(start.x + w, start.y)
        print(f"svg={svg}")
        return svg

    def svg_known(self, posn: Vector, scale: float):
        chars = ''.join(self.glyph_map.keys())
        return self.svg(posn, chars, scale)

    def birdfont_path(self, key, scale: float):
        g = self.glyph_map[key]
        return g.birdfont_path(self.fp, scale)

    def glyph_keys(self):
        return self.glyph_map.keys()
