from dataclasses import dataclass


@dataclass(frozen=True)
class FontParameters:
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

