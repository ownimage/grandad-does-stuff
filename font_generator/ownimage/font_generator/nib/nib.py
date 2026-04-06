from .nib_type import NibType


class Nib:
    @staticmethod
    def from_font_parameters(fp) -> "Nib":
        from .pen_nib import PenNib
        from .circle_nib import CircleNib
        from ..font_parameters import FontParameters
        if fp.nib_type == NibType.Pen:
            return PenNib.from_font_parameters(fp)
        else:
            return CircleNib.from_font_parameters(fp)

    def height(self) -> float:
        raise NotImplementedError()

    def below(self) -> float:
        raise NotImplementedError()
