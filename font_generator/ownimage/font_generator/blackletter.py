import math

from .compound_stroke import CompoundStroke
from .font_parameters import FontParameters
from .glyph import Glyph
from .mark import Mark
from .pen_nib import PenNib
from .stroke import Stroke
from .stroke_line import StrokeLine
from .stroke_type import StrokeType
from .vector import Vector


class Blackletter:
    def __init__(self, fp: FontParameters):
        self.fp = fp

        # calculated values
        r2 = math.sqrt(2)
        w = fp.pen_width
        t = fp.pen_thickness
        a = fp.ascender
        x = fp.x_height
        b = fp.baseline
        d = fp.descender
        m = w / (2 * r2) + t * (1 + r2) / 4
        h = (2 * w + (1 + 1 / r2) * t) / r2

        nib = PenNib.from_font_parameters(fp)
        f_dot = Stroke(nib.normal * (t - w))
        dot_width = f_dot.tr(fp).x - f_dot.bl(fp).x

        am1 = a - nib.tr.y
        am2 = a - nib.tr.y - (nib.direction * w).y

        xp1 = x + abs((nib.tr.x - nib.tl.x) * nib.normal.y / nib.normal.x) - nib.tl.y
        xp1 = x - f_dot.bl(fp).y
        xm1 = x - nib.tr.y
        xm2 = x - nib.tr.y - (nib.direction * w).y
        xm3 = x - nib.tr.y + f_dot.vec.y

        bp2 = b - nib.bl.y + (w - t) * nib.normal.y
        bp1 = b - nib.bl.y

        dp1 = d - nib.bl.y
        dp2 = d - nib.bl.y + w * nib.direction.y

        m1 = -nib.tl.x
        m2 = m1 + nib.direction.x * w
        m3 = m2 - nib.normal.x * (w - t)

        # m2 = 2 * m

        m4 = 4 * m
        m5 = 5 * m
        m6 = 6 * m
        m7 = 7 * m
        m8 = 8 * m
        m9 = 9 * m

        am_m = fp.ascender - m
        am_2m = fp.ascender - m2
        am_3m = fp.ascender - m3
        am_7m = fp.ascender - m7

        xp_m = fp.x_height + m
        xm_m = fp.x_height - m
        xm_2m = fp.x_height - m2
        xm_3m = fp.x_height - m3
        xm_4m = fp.x_height - m4
        xm_5m = fp.x_height - m5
        xm_7m = fp.x_height - m7

        bp = (1.5 * w + t) / r2
        bp_m = fp.baseline + m
        bp_2m = fp.baseline + m2
        bp_3m = fp.baseline + m3

        dp = d + (1.5 * w + t) / r2
        dp_3m = fp.descender + m3

        # flourishes

        f_f_footer = CompoundStroke([
            Stroke(nib.direction * -w - f_dot.vec, StrokeType.Move),
            f_dot
        ])

        f_i_footer = CompoundStroke([
            # Stroke.down(nib.bl.y, StrokeType.Extend),
            # Stroke(Vector(f_dot.vec.x * -.5, 2 * nib.bl.y - f_dot.bl(fp).y), StrokeType.Move),
            Stroke.down(-nib.bl.y - (-f_dot.bl(fp).y + f_dot.vec.y/2), StrokeType.Extend),
            Stroke(f_dot.vec * -0.5, StrokeType.Move),
            f_dot
        ])

        # strokes
        s_a1 = Stroke.down(xm2 - bp2)
        s_a2 = Stroke.down(x - nib.tr.y - 2 * nib.normal.y * (w - t) + nib.bl.y)

        s_b1 = Stroke.down(am1 - bp2)

        s_c1 = Stroke(nib.direction * w / 2, StrokeType.Move) + StrokeLine(nib.direction * w)

        s_d1 = Stroke.down(xm1 - bp2)
        s_d3 = Stroke(nib.normal * ((m3 - m1) / nib.normal.x))
        s_d4 = Stroke.down(xp1 + s_d3.vec.y - (nib.direction.y * w - nib.bl.y))

        s_f1 = Stroke.down(am2 - dp2)
        s_f2 = Stroke.right(3 * dot_width)

        s_g1 = Stroke.down(xm3 - dp2)

        s_h1 = Stroke.down(am1 - bp1)

        s_i1 = Stroke.down(xm1 - bp1)

        s_j1 = Stroke.down(xm1 - dp2)

        s_k1 = Stroke.right(m4)
        e_length = abs(w * nib.normal.x / nib.normal.y)
        k_height = max(fp.x_height / 2, x - f_dot.tr(fp).y + f_dot.bl(fp).y - abs(e_length * nib.direction.y))
        k_height = fp.x_height / 2
        s_k2 = Stroke.down(k_height - bp2)

        s_l1 = Stroke.down(am1 - bp2)

        s_m2 = Stroke.down(xm_4m)

        s_s1 = Stroke.down(m6)
        s_s2 = StrokeLine.right(m4)
        s_s3 = Stroke.down(fp.x_height - 10 * m)

        s_u1 = Stroke.down(xm_m - m3)

        s_x2 = Stroke.down(xm_m - bp_3m)

        s_z1 = Stroke.right(m4)
        s_z2 = StrokeLine(Vector(-m4, -m4))
        s_z3 = Stroke.down(xm_5m - dp)

        # compound strokes
        cs_a1 = s_a1 + f_dot
        cs_a2 = f_dot + s_a2 + f_dot

        cs_b1 = s_b1 + f_dot
        cs_b2 = f_dot + s_a1

        cs_c1 = s_a1 + f_dot + s_c1

        cs_d1 = s_d1 + f_dot
        cs_d2 = s_d3 + s_d4

        cs_e2 = f_dot + Stroke(nib.direction * -w / 2, StrokeType.Move) + StrokeLine(nib.direction * -e_length)

        cs_g1 = f_dot + s_g1

        cs_k1 = s_k1 + s_k2 + f_dot

        # cs_a2 = f_dot + s_a1.extend(t * r2) + f_dot

        cs_m2 = (f_dot + s_m2).add_after(f_i_footer)

        cs_x1 = s_k1 + s_x2 + f_dot

        # marks
        m_a1 = Mark(cs_a1, x=m1, y=xm2)
        m_a2 = Mark(cs_a2, x=m2, y=xm1)

        m_b1 = Mark(cs_b1, x=m1, y=am1)
        m_b2 = Mark(cs_b2, x=m2, y=xm1)

        m_c1 = Mark(cs_c1, x=m1, y=xm2)
        m_c2 = Mark(f_dot, x=m2, y=xm1)

        m_d1 = Mark(cs_d1, x=m1, y=xm1)
        m_d2 = Mark(cs_d2, x=m1, y=xp1)

        m_e2 = Mark(cs_e2, x=m2, y=xm1)

        m_f1 = Mark(CompoundStroke(s_f1).add_after(f_f_footer), x=m1, y=am2)
        m_f2 = Mark(f_dot, x=m2, y=am1)
        m_f3 = Mark(s_f2, x=m1 - 1.5 * dot_width, y=fp.tbar)

        m_g1 = Mark(cs_g1.add_after(f_f_footer), x=m2, y=xm1)

        m_h1 = Mark(CompoundStroke(s_h1).add_after(f_i_footer), x=m1, y=am1)

        m_i1 = Mark(CompoundStroke(s_i1).add_after(f_i_footer), x=m1, y=xm1)
        m_i_dot = Mark(f_dot, x=m1 - 0.5 * f_dot.vec.x, y=fp.tbar - 0.5 * f_dot.vec.y)

        m_j1 = Mark(CompoundStroke(s_j1).add_after(f_f_footer), x=m1, y=xm1)

        m_k1 = Mark(cs_k1, y=k_height)

        m_l1 = Mark(s_l1 + f_dot, x=m1, y=am1)

        m_m2 = Mark(cs_m2, x=m2, y=fp.x_height - m)
        m_m3 = m_a2.plus(Vector(m4, 0))  # this one stays as-is because it's a vector addition

        m_p1 = Mark(s_j1, y=xm_m)
        m_p3 = Mark(Stroke.from_xy(m4, -m4), x=-m2, y=m5)

        m_s1 = Mark((s_s1 + s_s2 + s_s3).add_after(f_f_footer), y=xm_m)

        m_u1 = Mark(s_u1 + f_dot, y=xm_m)
        m_u2 = Mark(s_u1 + f_dot, x=m4, y=xm_m)

        m_v2 = Mark(s_u1, x=m4, y=xm_m)

        m_w2 = Mark(s_u1 + f_dot, x=m4, y=xm_m)
        m_w3 = Mark(s_u1, x=m8, y=xm_m)
        m_w4 = Mark(s_k1, x=m2, y=xm_7m)

        m_x1 = Mark(cs_x1, y=xm_m)
        m_x2 = Mark(f_dot, y=m3)
        m_x3 = Mark(f_dot, x=m6, y=xm_m)

        m_z1 = Mark(s_z1, y=xm_m)
        m_z2 = Mark(s_z2, x=m4, y=xm_m)
        m_z3 = Mark((s_z1 + s_z3).add_after(f_f_footer), y=xm_5m)

        # glyphs
        default_width = 8 * m
        next = Vector(m4, 0)
        self.glyph_map = {
            'a': Glyph([m_a1, m_a2], default_width),
            'b': Glyph([m_b1, m_b2], default_width),
            'c': Glyph([m_c1, m_c2], default_width),
            'd': Glyph([m_d1, m_d2], default_width),
            'e': Glyph([m_c1, m_e2], default_width),
            'f': Glyph([m_f1, m_f2, m_f3], m4),
            'g': Glyph([m_a1, m_g1], default_width),
            'h': Glyph([m_h1, m_a2], m9),
            'i': Glyph([m_i1, m_i_dot], m4),
            'j': Glyph([m_j1, m_i_dot], m4),
            'k': Glyph([m_h1, m_c2, m_e2, m_k1], m9),
            'l': Glyph([m_l1], m5),
            'm': Glyph([m_i1, m_m2, m_m3], 13 * m),
            'n': Glyph([m_i1, m_a2], default_width),
            'o': Glyph([m_a1, m_b2], default_width),
            'p': Glyph([m_p1, m_b2, m_p3], default_width),
            'r': Glyph([m_i1, m_c2], m7),
            's': Glyph([m_s1, m_c2], m7),
            't': Glyph([m_l1, m_f3], m5),
            'u': Glyph([m_u1, m_u2], m9),
            'v': Glyph([m_u1, m_v2], default_width),
            'w': Glyph([m_u1, m_w2, m_w3, m_w4], 11 * m),
            'x': Glyph([m_x1, m_x2, m_x3, m_w4], 11 * m),
            'y': Glyph([m_u1, m_j1 + next], default_width),
            'z': Glyph([m_z1, m_z2, m_z3], default_width),
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
