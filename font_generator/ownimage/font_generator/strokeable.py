import math
from enum import Enum
from vector2d import Vector2D


class Strokeable:
    def __init__(self):
        pass

    def svg(self, start: Vector2D, scale: float, pen_thickness: float):
        raise RuntimeError("Not implemented yet")

    def birdfont_path(self, start: Vector2D, scale: float, pen_thickness: float):
        raise RuntimeError("Not implemented yet")

