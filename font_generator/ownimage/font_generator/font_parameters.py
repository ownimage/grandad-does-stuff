from dataclasses import dataclass

from ownimage.font_generator.nib_type import NibType


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

