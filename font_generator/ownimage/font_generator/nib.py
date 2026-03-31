
from .font_parameters import FontParameters


class Nib:
    @staticmethod
    def from_font_parameters(fp: FontParameters) -> "Nib":
        from .pen_nib import PenNib
        from .circle_nib import CircleNib
        if fp.nib_type == "Pen":
            return PenNib.from_font_parameters(fp)
        else:
            return CircleNib.from_font_parameters(fp)