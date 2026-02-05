from shapely.geometry import Point

from .font_parameters import FontParameters
from .strokeable import Strokeable

class CompoundStroke(Strokeable):
    def __init__(self, strokes: list[Strokeable]):
        super().__init__()
        self.strokes = strokes


    def svg(self, posn: Point, fp: FontParameters, scale: float):
        svg = ""
        start = posn
        for stroke in self.strokes:
            start, s = stroke.svg(start, fp, scale)
            svg += s
        return start, svg

    def birdfont_path(self, start: Point, fp: FontParameters, scale: float):
        paths = []

        for stroke in self.strokes:
            start, new_paths = stroke.birdfont_path(start, fp, scale)
            paths += new_paths
        return start, paths

