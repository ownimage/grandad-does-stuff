from dataclasses import dataclass, replace
from functools import cached_property
from math import cos, sin, radians

from ..nib import Nib
from ..vector import Vector


@dataclass(frozen=True)
class CircleNib(Nib):
    size: float
    pos: Vector = Vector.zero()
    num_samples: int = 20

    @staticmethod
    def from_font_parameters(fp: "FontParameters") -> "CircleNib":
        return CircleNib(fp.pen_width / 2)

    def moved_to(self, x: float, y: float) -> "CircleNib":
        """Return a new nib at a new position."""
        return CircleNib(self.size, Vector(x, y))

    def at(self, pos: Vector) -> "CircleNib":
        return replace(self, pos=pos)

    @cached_property
    def outline(self) -> list[Vector]:
        """Return an array of vectors for points on a circle centered at pos with radius size."""
        return [
            self.pos + Vector(
                self.size * cos(2 * radians(i * 360 / self.num_samples)),
                self.size * sin(2 * radians(i * 360 / self.num_samples))
            )
            for i in range(self.num_samples)
        ]

    def height(self) -> float:
        return self.size * 2

    def below(self) -> float:
        return -self.size

    # Named points (top-left, left, bottom-left, bottom, bottom-right, right, top-right, top)
    @cached_property
    def tl(self): return self.pos + Vector.tl(self.size)

    @cached_property
    def l(self):  return self.pos + Vector.l(self.size)

    @cached_property
    def bl(self): return self.pos + Vector.bl(self.size)

    @cached_property
    def b(self):  return self.pos + Vector.b(self.size)

    @cached_property
    def t(self):  return self.pos + Vector.l(self.size)

    @cached_property
    def br(self): return self.pos + Vector.br(self.size)

    @cached_property
    def r(self):  return self.pos + Vector.r(self.size)

    @cached_property
    def tr(self): return self.pos + Vector.t(self.size)
