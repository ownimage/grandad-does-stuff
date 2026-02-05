from vector2d import Vector2D

from .font_parameters import FontParameters


class Strokeable:
    def __init__(self):
        pass

    def svg(self, start: Vector2D, fp: FontParameters, scale: float):
        raise RuntimeError("Not implemented yet")

    def birdfont_path(self, start: Vector2D, fp: FontParameters, scale: float):
        raise RuntimeError("Not implemented yet")

