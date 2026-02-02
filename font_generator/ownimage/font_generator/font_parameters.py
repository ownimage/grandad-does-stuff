from dataclasses import dataclass


@dataclass(frozen=True)
class FontParameters:
    pen_thickness: float
    baseline: float
    x_height: float
    ascender: float
