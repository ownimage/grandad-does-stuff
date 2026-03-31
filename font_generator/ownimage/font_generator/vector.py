from dataclasses import dataclass
import math
from typing import Tuple


@dataclass(frozen=True)
class Vector:
    x: float = 0.0
    y: float = 0.0

    @staticmethod
    def zero() -> "Vector":
        return Vector(0, 0)

    @staticmethod
    def tl(length: float = 1) -> "Vector":
        act = length / math.sqrt(2)
        return Vector(-act, act)

    @staticmethod
    def tr(length: float = 1) -> "Vector":
        act = length / math.sqrt(2)
        return Vector(act, act)

    @staticmethod
    def bl(length: float = 1) -> "Vector":
        act = length / math.sqrt(2)
        return Vector(-act, -act)

    @staticmethod
    def br(length: float = 1) -> "Vector":
        act = length / math.sqrt(2)
        return Vector(act, -act)

    @staticmethod
    def r(length: float = 1) -> "Vector":
        return Vector(length, 0)

    @staticmethod
    def l(length: float = 1) -> "Vector":
        return Vector(-length, 0)

    @staticmethod
    def t(length: float = 1) -> "Vector":
        return Vector(0, length)

    @staticmethod
    def b(length: float = 1) -> "Vector":
        return Vector(0, -length)

    @staticmethod
    def of(p) -> "Vector":
        if isinstance(p, Vector):
            return p
        if isinstance(p, (tuple, list)) and len(p) == 2:
            return Vector(float(p[0]), float(p[1]))
        raise TypeError(f"Cannot convert {p!r} to Vector")

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def length(self):
        return math.hypot(self.x, self.y)

    def normalized(self):
        l = self.length()
        return Vector(self.x / l, self.y / l) if l else Vector(0, 0)

    def rotated(self, degrees):
        r = math.radians(degrees)
        c = math.cos(r)
        s = math.sin(r)
        return Vector(self.x * c - self.y * s,
                    self.x * s + self.y * c)

    def cross(self, other: "Vector") -> float:
        """2D cross product (returns scalar)."""
        return self.x * other.y - self.y * other.x

    def xy(self)-> Tuple[float, float]:
        return self.x, self.y
