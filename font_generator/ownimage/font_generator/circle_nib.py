from dataclasses import dataclass, replace
from math import cos, sin, radians

from .nib import Nib
from .vector import Vector


@dataclass(frozen=True)
class CircleNib(Nib):
    size: float
    pos: Vector = Vector.zero()
    num_samples: int = 20

    def moved_to(self, x: float, y: float) -> "CircleNib":
        """Return a new nib at a new position."""
        return CircleNib(self.size, Vector(x, y))

    def at(self, pos: Vector) -> "CircleNib":
        return replace(self, pos=pos)

    def outline(self) -> list[Vector]:
        """Return an array of vectors for points on a circle centered at pos with radius size."""
        return [
            self.pos + Vector(
                self.size * cos(2 * radians(i * 360 / self.num_samples)),
                self.size * sin(2 * radians(i * 360 / self.num_samples))
            )
            for i in range(self.num_samples)
        ]
