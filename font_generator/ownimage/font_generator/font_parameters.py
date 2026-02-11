from dataclasses import dataclass


@dataclass(frozen=True)
class FontParameters:
    pen_thickness: float
    filled: bool
    ascender: float
    tbar: float
    x_height: float
    baseline: float
    descender: float
    line_thickness: float
