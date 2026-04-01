
from .font_parameters import FontParameters
from .nib_type import NibType


class Nib:
    @staticmethod
    def from_font_parameters(fp: FontParameters) -> "Nib":
        from .pen_nib import PenNib
        from .circle_nib import CircleNib
        if fp.nib_type == NibType.Pen:
            return PenNib.from_font_parameters(fp)
        else:
            return CircleNib.from_font_parameters(fp)