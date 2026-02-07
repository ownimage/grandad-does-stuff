import math
from shapely.geometry import Point

from .compound_stroke import CompoundStroke
from .font_parameters import FontParameters
from .stroke import Stroke
from .mark import Mark
from .glyph import Glyph


class Blackletter:
    def __init__(self, fp: FontParameters):
        self.fp = fp

        # calculated values
        m = fp.pen_thickness / (2 * math.sqrt(2))
        m2 = 2 * m
        m3 = 3 * m
        m4 = 4 * m

        am_m = fp.ascender - m
        am_3m = fp.ascender -m3
        am_7m = fp.ascender - 7 * m

        xp_m = fp.x_height + m
        xm_m = fp.x_height - m
        xm_3m = fp.x_height - m3
        xm_7m = fp.x_height - 7 * m

        bp_m = fp.baseline + m
        bp_2m = fp.baseline + m2
        bp_3m = fp.baseline + m3

        dp_3m = fp.descender + m3

        # flourishes
        f_dot = Stroke(Point(m2, -m2))

        f_f_footer = CompoundStroke([
            Stroke(Point(-m4, 0), Stroke.StrokeType.Move),
            f_dot
        ])

        f_h_footer = CompoundStroke([
            Stroke(Point(0, m), Stroke.StrokeType.Extend),
            Stroke(Point(-m, m), Stroke.StrokeType.Move),
            f_dot
        ])

        # strokes
        s_a1 = Stroke(Point(0, bp_3m - xm_3m))

        s_b1 = Stroke(Point(0, bp_3m - am_m))

        s_c1 = Stroke(Point(m2, m2))

        s_d1 = Stroke(Point(m4, -m4))

        s_f1 = Stroke(Point(0, dp_3m - am_3m))
        s_f2 = Stroke(Point(6 * m, 0))

        s_g1 = Stroke(Point(0, dp_3m - xm_3m))

        s_h1 = Stroke(Point(0, 0 - (fp.ascender - 2 * m)))

        s_i1 = Stroke(Point(0, m - xm_m))

        s_j1 = Stroke(Point(0, dp_3m - xm_m))

        s_k1 = Stroke(Point(4 * m, 0))
        s_k2 = Stroke(Point(0, 9 * m - fp.x_height))

        # compound strokes
        cs_a1 = CompoundStroke([s_a1, f_dot])
        cs_a2 = CompoundStroke([f_dot, s_a1, f_dot])

        cs_b1 = CompoundStroke([s_b1, f_dot])
        cs_b2 = CompoundStroke([f_dot, s_a1])

        cs_c1 = CompoundStroke([s_a1, f_dot, s_c1])

        cs_g1 = CompoundStroke([f_dot, s_g1])

        cs_k1 = CompoundStroke([s_k1, s_k2])

        # marks
        m_a1 = Mark(Point(0, xm_3m), [cs_a1])
        m_a2 = Mark(Point(2 * m, xm_m), [cs_a2])

        m_b1 = Mark(Point(0, am_m), [cs_b1])
        m_b2 = Mark(Point(2 * m, xm_m), [cs_b2])

        m_c1 = Mark(Point(0, xm_3m), [cs_c1])
        m_c2 = Mark(Point(2 * m, xm_m), [f_dot])

        m_d1 = Mark(Point(0, xp_m, 0), [s_d1, s_a1])

        m_e1 = Mark(Point(0, xm_7m), [s_c1])

        m_f1 = Mark(Point(0, am_3m), [CompoundStroke([s_f1]).add_after(f_f_footer)])
        m_f2 = Mark(Point(2 * m, am_m), [f_dot])
        m_f3 = Mark(Point(-3 * m, am_7m), [s_f2])

        m_g1 = Mark(Point(2 * m, xm_m), [cs_g1.add_after(f_f_footer)])

        m_h1 = Mark(Point(0, fp.ascender - m), [CompoundStroke([s_h1]).add_after(f_h_footer)])

        m_i1 = Mark(Point(0, fp.x_height - m), [CompoundStroke([s_i1]).add_after(f_h_footer)])
        m_i2 = Mark(Point(-m, fp.x_height + 3 * m), [f_dot])

        m_j1 = Mark(Point(0, fp.x_height - m), [s_j1])
        m_j2 = Mark(Point(-4 * m, dp_3m), [f_dot])

        m_k1 = Mark(Point(0, fp.x_height - 7 * m), [cs_k1])

        # glyphs
        self.glyph_map = {
            'a': Glyph(Point(0, 0), [m_a1, m_a2]),
            'b': Glyph(Point(0, 0), [m_b1, m_b2]),
            'c': Glyph(Point(0, 0), [m_c1, m_c2]),
            'd': Glyph(Point(0, 0), [m_a1, m_d1]),
            'e': Glyph(Point(0, 0), [m_c1, m_c2, m_e1]),
            'f': Glyph(Point(0, 0), [m_f1, m_f2, m_f3]),
            'g': Glyph(Point(0, 0), [m_a1, m_g1]),
            'h': Glyph(Point(0, 0), [m_h1, m_a2]),
            'i': Glyph(Point(0, 0), [m_i1, m_i2]),
            'j': Glyph(Point(0, 0), [m_j1, m_j2, m_i2]),
            'k': Glyph(Point(0, 0), [m_h1, m_c2, m_e1, m_k1]),
            'l': Glyph(Point(0, 0), [m_h1])
        }

        self.glyph_widths = {'default': 8 * m, 'c': 6 * m, 'f': 4 * m, 'h': 9 * m, 'i': 4 * m, 'j': 4 * m}

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
