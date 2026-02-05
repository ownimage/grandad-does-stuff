from shapely.geometry import Point

from .font_parameters import FontParameters


class Strokeable:
    def __init__(self):
        pass

    def svg(self, start: Point, fp: FontParameters, scale: float):
        raise RuntimeError("Not implemented yet")

    def birdfont_path(self, start: Point, fp: FontParameters, scale: float):
        raise RuntimeError("Not implemented yet")

