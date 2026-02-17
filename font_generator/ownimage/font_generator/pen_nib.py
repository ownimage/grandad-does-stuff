from dataclasses import dataclass, field
from math import cos, sin, radians
from typing import Tuple

from font_generator.ownimage.font_generator.vector import Vector


@dataclass(frozen=True)
class PenNib:
    width: float
    thickness: float
    angle: float                 # degrees, 0° = horizontal
    pos: Vector = field(default_factory=lambda: Vector(0, 0))

    # Computed fields
    direction: Vector = field(init=False)
    normal: Vector = field(init=False)

    def __post_init__(self):
        # Unit direction vector from angle
        dx = cos(radians(self.angle))
        dy = sin(radians(self.angle))
        object.__setattr__(self, "direction", Vector(dx, dy).normalized())

        # Perpendicular (unit normal)
        nx = -dy
        ny = dx
        object.__setattr__(self, "normal", Vector(nx, ny).normalized())

    # --- Corner helpers -----------------------------------------------------

    def _corner(self, dx: float, dy: float) -> Vector:
        """Return pos + dx*direction + dy*normal."""
        return self.pos + self.direction * dx + self.normal * dy

    # Named points (top-left, left, bottom-left, bottom, bottom-right, right, top-right, top)
    @property
    def tl(self): return self._corner(-self.width/2,  self.thickness/2)
    @property
    def l(self):  return self._corner(-self.width/2,  0)
    @property
    def bl(self): return self._corner(-self.width/2, -self.thickness/2)

    @property
    def b(self):  return self._corner(0, -self.thickness/2)
    @property
    def t(self):  return self._corner(0,  self.thickness/2)

    @property
    def br(self): return self._corner(self.width/2, -self.thickness/2)
    @property
    def r(self):  return self._corner(self.width/2,  0)
    @property
    def tr(self): return self._corner(self.width/2,  self.thickness/2)

    # --- Move / copy --------------------------------------------------------

    def moved_to(self, x: float, y: float) -> "PenNib":
        """Return a new nib at a new position."""
        return PenNib(self.width, self.thickness, self.angle, Vector(x, y))