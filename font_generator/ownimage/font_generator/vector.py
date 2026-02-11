from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Vector:
    x: float = 0.0
    y: float = 0.0

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

    def rotated(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return Vector(self.x * c - self.y * s,
                    self.x * s + self.y * c)