from .bezier_stroke import BezierStroke
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
        pen_width = fp.pen_width
        pen_thickness = fp.pen_thickness
        a = fp.ascender
        t = fp.tbar
        x = fp.x_height
        b = fp.baseline
        d = fp.descender

        nib = PenNib.from_font_parameters(fp)
        f_dot = Stroke(nib.normal * (pen_thickness - pen_width))

        def f_v_dot_chain(n: int):
            link = f_dot + Stroke(Vector(0, f_dot.bl(fp).y - f_dot.tr(fp).y) - f_dot.vec, StrokeType.Move)
            r = link
            for i in range(n - 1):
                r = r + link
            return r

        am = Mark(f_dot).top_at(a, fp)
        xm = Mark(f_dot).top_at(x, fp)
        xb2 = x / 2
        bp = Mark(f_dot).bottom_at(b, fp)

        # flourishes
        f_f_footer = CompoundStroke([
            Stroke(nib.direction * -pen_width - f_dot.vec, StrokeType.Move),
            f_dot
        ])

        f_i_footer = CompoundStroke([
            Stroke(f_dot.vec * -0.5, StrokeType.Move),
            f_dot
        ])

        f_i_dot = Mark(f_dot, x=0.5 * f_dot.vec.x, y=fp.tbar - 0.5 * f_dot.vec.y)

        # glyphs
        self.glyph_map = {}

        # A
        m_A1 = (
            Mark(
                Stroke.down(a - t)
                +
                BezierStroke.from_four_points(
                    Vector(0, x / 3),
                    Vector(0, 0),
                    Vector(-4 * pen_width, 0),
                    Vector(-4 * pen_width, x / 3),  # end point
                    num_samples=20,
                    debug_visual=True
                )
            )
            .top_at(a - 2 * pen_width, fp)
            .extend_downstroke_to_set_bottom_at(0, b, fp)
        )
        m_A2 = (Mark(BezierStroke.horizontal_flourish(6 * pen_width, pen_width / 2, -pen_width * 3))
                .top_at(a, fp)
                )
        m_A3 = (Mark(f_dot)
                .top_at(x, fp)
                .left_at(f_dot.tr(fp).x, fp)
                )
        m_A4 = (Mark(f_v_dot_chain(3))
                .top_at(x, fp)
                .right_at(f_dot.tl(fp).x, fp)
                )
        m_A4 = m_A4.down_by(m_A4.bounding_box(fp).cy - m_A3.stroke_bounding_box(0, fp).cy)
        m_A5 = (Mark(Stroke.down() + f_i_footer)
                .left_by(f_dot.tl(fp).x - m_A3.bounding_box(fp).right)
                .start_at_bezier(fp, m_A2)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        self.glyph_map['A'] = Glyph([m_A1, m_A2, m_A3, m_A4, m_A5], fp)

        # B
        m_B2 = (Mark(BezierStroke.horizontal_flourish(6 * pen_width, pen_width / 2))
                .top_at(a, fp)
                )
        self.glyph_map['B'] = Glyph([m_B2], fp)
        # a
        m_a1 = (Mark(Stroke.down() + f_dot)
                .top_at(xm.stroke_tl(0, fp).y, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_a2 = (Mark(f_dot + Stroke.down() + f_dot)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(1, b, fp)
                .left_at(m_a1.stroke_tr(0, fp).x, fp)
                )
        self.glyph_map['a'] = Glyph([m_a1, m_a2], fp)

        # b
        m_b1 = (Mark(Stroke.down() + f_dot)
                .top_at(a, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_b2 = (Mark(f_dot + Stroke.down())
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(1, bp.stroke_br(0, fp).y, fp)
                .left_at(m_b1.stroke_tr(0, fp).x, fp)
                )
        self.glyph_map['b'] = Glyph([m_b1, m_b2], fp)

        # c
        s_c1 = Stroke(nib.direction * pen_width / 2, StrokeType.Move) + StrokeLine(nib.direction * pen_width)
        m_c1 = (Mark(Stroke.down() + f_dot + s_c1)
                .top_at(xm.stroke_tl(0, fp).y, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_c2 = (Mark(f_dot)
                .top_at(x, fp)
                .left_at(m_a1.stroke_tr(0, fp).x, fp)
                )
        self.glyph_map['c'] = Glyph([m_c1, m_c2], fp)

        # d
        m_d1 = m_a1
        m_d2 = (Mark(f_dot + Stroke.down())
                .top_at(x, fp)
                .left_at(m_d1.stroke_tr(0, fp).x, fp)
                .extend_downstroke_to_set_bottom_at(1, bp.stroke_br(0, fp).y, fp)
                .extend_stroke_backwards_to_x(0, m_d1.stroke_tl(0, fp).x, fp)
                )
        self.glyph_map['d'] = Glyph([m_d1, m_d2], fp)

        # e
        s_e1 = Stroke(nib.direction * pen_width / 2, StrokeType.Move) + StrokeLine(nib.direction * pen_width)
        m_e1 = (Mark(Stroke.down() + f_dot + s_e1)
                .top_at(xm.stroke_tl(0, fp).y, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_e2 = (Mark(f_dot + Stroke(nib.direction * -pen_width / 2, StrokeType.Move) + StrokeLine(nib.direction * -pen_width))
                .top_at(x, fp)
                .left_at(m_a1.stroke_tr(0, fp).x, fp)
                )
        self.glyph_map['e'] = Glyph([m_e1, m_e2], fp)

        # f
        m_f1 = (Mark(Stroke.down() + f_f_footer)
                .top_at(am.stroke_tl(0, fp).y, fp)
                .extend_downstroke_to_set_bottom_at(0, d, fp)
                )
        m_f3 = am.left_at(m_f1.stroke_tr(0, fp).x, fp)
        s_f4 = (Stroke.right()
                .make_width(m_f1.bounding_box(fp).width + m_f3.bounding_box(fp).width, fp)
                )
        m_f4 = (Mark(s_f4, Vector(0, t))
                .left_at(m_f1.bounding_box(fp).left, fp)
                )
        self.glyph_map['f'] = Glyph([m_f1, m_f3, m_f4], fp)

        # g
        m_g1 = (Mark(Stroke.down() + f_dot)
                .top_at(xm.stroke_tl(0, fp).y, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_g2 = (Mark(f_dot + Stroke.down() + f_f_footer)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(1, d, fp)
                .left_at(m_g1.bounding_box(fp).left, fp)
                )
        self.glyph_map['g'] = Glyph([m_g1, m_g2], fp)

        # h
        m_h1 = (Mark(Stroke.down() + f_i_footer)
                .top_at(t, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_h2 = (Mark(f_dot + Stroke.down() + f_dot)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(1, b, fp)
                .left_at(m_h1.stroke_tr(1, fp).x, fp)
                )
        self.glyph_map['h'] = Glyph([m_h1, m_h2], fp)

        # i
        m_i1 = (Mark(Stroke.down() + f_i_footer)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_i2 = (f_i_dot
                .centre_x_at(m_i1.vec.x, fp)
                )
        self.glyph_map['i'] = Glyph([m_i1, m_i2], fp)

        # j
        m_j1 = (Mark(Stroke.down() + f_f_footer)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, d, fp)
                )
        m_j2 = (f_i_dot
                .centre_x_at(m_j1.vec.x, fp)
                )
        self.glyph_map['j'] = Glyph([m_j1, m_j2], fp)

        # k
        m_k1 = (Mark(Stroke.down() + f_i_footer)
                .top_at(t, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_k2 = m_e2
        m_k3 = (Mark(Stroke.right(xm.bounding_box(fp).width) + Stroke.down() + f_dot)
                .top_at(xb2, fp)
                .extend_downstroke_to_set_bottom_at(1, b, fp)
                )
        self.glyph_map['k'] = Glyph([m_k1, m_k2, m_k3], fp)

        # l
        m_l1 = (Mark(Stroke.down() + f_dot).top_at(a, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        self.glyph_map['l'] = Glyph([m_l1], fp)

        # m
        m_m1 = (Mark(Stroke.down() + f_i_footer).top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_m2 = (Mark(f_dot + Stroke.down() + f_i_footer)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(1, b, fp)
                .left_at(m_h1.stroke_tr(1, fp).x, fp)
                )
        m_m3 = (Mark(f_dot + Stroke.down() + f_dot)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(1, b, fp)
                .left_at(m_m2.stroke_tr(1, fp).x, fp)
                )
        self.glyph_map['m'] = Glyph([m_m1, m_m2, m_m3], fp)

        # n
        m_n1 = (Mark(Stroke.down() + f_i_footer)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_n2 = m_h2
        self.glyph_map['n'] = Glyph([m_n1, m_n2], fp)

        # o
        m_o1 = m_a1
        m_o2 = m_b2
        self.glyph_map['o'] = Glyph([m_o1, m_o2], fp)

        # p
        m_p1 = (Mark(Stroke.down())
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, d, fp)
                )
        m_p2 = (Mark(f_dot + Stroke.down())
                .top_at(x, fp)
                .left_at(m_p1.stroke_tr(0, fp).x, fp)
                .extend_downstroke_to_set_bottom_at(1, b, fp)
                )
        m_p3 = (Mark(f_dot)
                .bottom_at(b, fp)
                .left_at(m_p2.bounding_box(fp).left, fp)
                .extend_stroke_backwards_to_x(0, -m_i2.bounding_box(fp).width / 2, fp)
                )
        self.glyph_map['p'] = Glyph([m_p1, m_p2, m_p3], fp)

        # q
        m_q1 = m_a1
        m_q2 = (Mark(f_dot + Stroke.down())
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(1, d, fp)
                .left_at(m_o1.stroke_tr(0, fp).x, fp)
                )
        self.glyph_map['q'] = Glyph([m_q1, m_q2], fp)

        # r
        m_r1 = (Mark(Stroke.down() + f_i_footer)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_r2 = (f_i_dot
                .top_at(x, fp)
                .left_at(m_r1.stroke_tr(1, fp).x, fp)
                )
        self.glyph_map['r'] = Glyph([m_r1, m_r2], fp)

        # s
        sw = xm.bounding_box(fp).width
        m_s1 = (Mark(Stroke.down(xm.vec.y - xb2) + StrokeLine(Vector(sw, 0)) + Stroke.down() + f_f_footer)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(2, b, fp)
                )
        m_s2 = (xm
                .left_at(m_s1.stroke_tr(0, fp).x, fp)
                )

        self.glyph_map['s'] = Glyph([m_s1, m_s2], fp)

        # t
        m_t1 = (Mark(Stroke.down() + f_dot)
                .top_at(a, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_t2 = m_f4
        self.glyph_map['t'] = Glyph([m_t1, m_t2], fp)

        # u
        m_u1 = (Mark(Stroke.down() + f_dot)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_u2 = (Mark(Stroke.down())
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, m_u1.stroke_br(1, fp).y, fp)
                .left_at(m_u1.bounding_box(fp).right, fp)
                )
        self.glyph_map['u'] = Glyph([m_u1, m_u2], fp)

        # v
        m_v1 = (Mark(Stroke.down() + f_dot)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                )
        m_v2 = (Mark(Stroke.down() + f_dot)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                .left_at(m_v1.bounding_box(fp).right, fp)
                )
        self.glyph_map['v'] = Glyph([m_v1, m_v2], fp)

        # w
        m_w1 = m_u1
        m_w2 = (Mark(Stroke.down() + f_dot)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, b, fp)
                .left_at(m_w1.bounding_box(fp).right, fp)
                )
        m_w3 = (Mark(Stroke.down()).top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(0, m_w2.stroke_br(1, fp).y, fp)
                .left_at(m_w2.bounding_box(fp).right, fp)
                )
        m_w4 = (Mark(Stroke.right(), Vector(0, xb2))
                .left_at(m_w1.stroke_tr(0, fp).x, fp)
                .extend_rightstroke_to_set_right_at(0, m_w3.stroke_bl(0, fp).x, fp)
                )
        self.glyph_map['w'] = Glyph([m_w1, m_w2, m_w3, m_w4], fp)

        # x
        m_x1 = xm
        m_x2 = bp
        m_x3 = (m_u1
                .left_at(m_w1.bounding_box(fp).right, fp)
                )
        m_x4 = (xm
                .left_at(m_x3.stroke_tr(0, fp).x, fp)
                )
        m_x5 = m_w4
        self.glyph_map['x'] = Glyph([m_x1, m_x2, m_x3, m_x4, m_x5], fp)

        # y
        m_y1 = m_u1
        m_y2 = (m_j1
                .left_at(m_y1.bounding_box(fp).left, fp)
                )
        self.glyph_map['y'] = Glyph([m_y1, m_y2], fp)

        # z
        zw = xm.bounding_box(fp).width
        m_z1 = (Mark(Stroke.right(zw) + StrokeLine(Vector(-zw, -zw)) + Stroke.right(zw) + Stroke.down() + f_f_footer)
                .top_at(x, fp)
                .extend_downstroke_to_set_bottom_at(3, d, fp)
                )
        self.glyph_map['z'] = Glyph([m_z1], fp)

    def svg(self, start: Vector, chars: str, scale: float, char_lines: bool = False):

        def _char_line(x: float, scale: float) -> str:
            xs = x * scale
            return f'<line x1="{xs}" y1="{self.fp.descender * scale}" x2="{xs}" y2="{self.fp.ascender * scale}" stroke="black" stroke-width="1" />\n'

        svg = ""
        start = start
        for c in chars:
            g: Glyph = self.glyph_map[c]
            svg += f"<!-- char {c} -->\n"
            if char_lines:
                svg += _char_line(start.x, scale)
            svg += g.svg(start, self.fp, scale)
            w = g.width
            start = Vector(start.x + w, start.y)
            if char_lines:
                svg += _char_line(start.x, scale)
            start = Vector(start.x + self.fp.padding, start.y)

        if char_lines:
            svg += _char_line(start.x, scale)
        print(f"svg={svg}")
        return svg

    def svg_known(self, start: Vector, scale: float, char_lines: bool = False):
        chars = ''.join(self.glyph_map.keys())
        return self.svg(start, chars, scale, char_lines)

    def birdfont_path(self, key, scale: float):
        g = self.glyph_map[key]
        return g.birdfont_path(self.fp, scale)

    def glyph_keys(self):
        return self.glyph_map.keys()
