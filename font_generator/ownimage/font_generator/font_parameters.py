from dataclasses import dataclass
from functools import cached_property

from .nib.nib_type import NibType


@dataclass(frozen=True)
class FontParameters:
    nib_type: NibType
    pen_width: float
    pen_thickness: float
    pen_angle: float
    filled: bool
    ascender: float
    tbar: float
    x_height: float
    baseline: float
    descender: float
    padding: float
    pen_stroke: list[tuple[float, float]]
    bezier_samples: int
    circle_samples: int

    @cached_property
    def nib(self) -> "Nib":
        from .nib import Nib
        return Nib.from_font_parameters(self)

    @cached_property
    def pen_nib(self) -> "Nib":
        from .nib.pen_nib import PenNib
        return PenNib.from_font_parameters(self)

    @cached_property
    def circle_nib(self) -> "Nib":
        from .nib.circle_nib import CircleNib
        return CircleNib.from_font_parameters(self)


