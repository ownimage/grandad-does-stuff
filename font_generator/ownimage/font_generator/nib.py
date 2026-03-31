
from .font_parameters import FontParameters


class Nib:
    @staticmethod
    def from_font_parameters(fp: FontParameters) -> "Nib":
        from .pen_nib import PenNib
        from .circle_nib import CircleNib
        if fp.nib_type == "Pen":
            return PenNib(fp.pen_width, fp.pen_thickness, fp.pen_angle)
        else:
            return CircleNib(fp.pen_width)