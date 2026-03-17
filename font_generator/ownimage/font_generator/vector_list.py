from typing import List, Tuple
from .vector import Vector


class VectorList:

    @staticmethod
    def from_list_of_tuples(points: list[Tuple[float, float]]) -> List[Vector]:
        return [Vector(p[0], p[1]) for p in points]

    @staticmethod
    def to_list_of_xy(vectors: list[Vector]) -> List[Tuple[float, float]]:
        return [v.xy() for v in vectors]
