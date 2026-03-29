from __future__ import annotations

from typing import Union, List

from .stroke import Stroke
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector import Vector


class LineStroke(Strokeable):

    def __init__(self, vec: Vector):
        super().__init__(StrokeType.Line)
        self.vec = vec

    @staticmethod
    def from_xy(x: float, y: float) -> LineStroke:
        return LineStroke(Vector(x, y))

    @staticmethod
    def between(start: Vector, end: Vector) -> LineStroke:
        return LineStroke(start - end)

    @staticmethod
    def right(length: float) -> LineStroke:
        return LineStroke(Vector(length, 0))

    @staticmethod
    def down(length: float) -> LineStroke:
        return LineStroke(Vector(0, -length))

    def extend(self, e: Union[Stroke, Vector, float]) -> LineStroke:
        if isinstance(e, Stroke):
            if e.stroke_type == StrokeType.Extend:
                return LineStroke(self.vec + e.vec)
            raise RuntimeError("Can only extend by a Stroke of type Extend.")

        if isinstance(e, Vector):
            return LineStroke(self.vec + e)

        if isinstance(e, float):
            return LineStroke(self.vec + e * self.vec.normalized())

        raise RuntimeError(f"Extension type of {type(e)}.")

    def sample_points(self, start: Vector, num_samples: int = 20) -> List[Vector]:
        points = []
        for i in range(num_samples):
            t = i / (num_samples - 1)
            points.append(start + self.vec * t)
        return points
