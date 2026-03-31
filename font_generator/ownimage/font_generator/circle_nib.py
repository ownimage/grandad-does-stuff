from dataclasses import dataclass, replace
from math import cos, sin, radians

from .font_parameters import FontParameters
from .nib import Nib
from .vector import Vector


@dataclass(frozen=True)
class CircleNib(Nib):
    size: float
    pos: Vector = Vector.zero()
    num_samples: int = 20

    @staticmethod
    def from_font_parameters(fp: FontParameters) -> "CircleNib":
        return CircleNib(fp.pen_width / 2)

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

    # Named points (top-left, left, bottom-left, bottom, bottom-right, right, top-right, top)
    @property
    def tl(self): return self.pos + Vector.tl(self.size)

    @property
    def l(self):  return self.pos + Vector.l(self.size)

    @property
    def bl(self): return self.pos + Vector.bl(self.size)

    @property
    def b(self):  return self.pos + Vector.b(self.size)

    @property
    def t(self):  return self.pos + Vector.l(self.size)

    @property
    def br(self): return self.pos + Vector.br(self.size)

    @property
    def r(self):  return self.pos + Vector.r(self.size)

    @property
    def tr(self): return self.pos + Vector.t(self.size)
