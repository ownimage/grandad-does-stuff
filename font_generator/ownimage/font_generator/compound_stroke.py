from vector2d import Vector2D

from .font_parameters import FontParameters
from .strokeable import Strokeable

class CompoundStroke(Strokeable):
    def __init__(self, strokes: list[Strokeable]):
        super().__init__()
        self.strokes = strokes


    def svg(self, posn: Vector2D, fp: FontParameters, scale: float):
        svg = ""
        start = posn
        for stroke in self.strokes:
            start, s = stroke.svg(start, fp, scale)
            svg += s
        return start, svg

    def birdfont_path(self, start: Vector2D, scale: float, pen_thickness: float):
        raise RuntimeError("Not implemented yet")

