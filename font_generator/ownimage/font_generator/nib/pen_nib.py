from dataclasses import dataclass, field
from math import cos, sin, radians

from ownimage.font_generator.font_parameters import FontParameters
from ownimage.font_generator.nib import Nib
from ownimage.font_generator.vector import Vector


@dataclass(frozen=True)
class PenNib(Nib):
    width: float
    thickness: float
    angle: float  # degrees, 0° = horizontal
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

    @staticmethod
    def from_font_parameters(fp: FontParameters) -> "PenNib":
        return PenNib(fp.pen_width, fp.pen_thickness, fp.pen_angle)

    def height(self) -> float:
        y_corners = [self.tl.y, self.tr.y, self.br.y, self.bl.y]
        return max(y_corners) - min(y_corners)

    def below(self) -> float:
        y_corners = [self.tl.y, self.tr.y, self.br.y, self.bl.y]
        return -min(y_corners) + self.pos.y

    def at(self, pos: Vector) -> "PenNib":
        return PenNib(
            width=self.width,
            thickness=self.thickness,
            angle=self.angle,
            pos=pos
        )

    def move(self, delta: Vector) -> "PenNib":
        return PenNib(
            width=self.width,
            thickness=self.thickness,
            angle=self.angle,
            pos=self.pos + delta
        )

    # --- Corner helpers -----------------------------------------------------

    def _offset(self, dx: float, dy: float) -> Vector:
        """Return pos + dx*direction + dy*normal."""
        return self.pos + self.direction * dx + self.normal * dy

    # Named points (top-left, left, bottom-left, bottom, bottom-right, right, top-right, top)
    @property
    def tl(self): return self._offset(-self.width / 2, self.thickness / 2)

    @property
    def l(self):  return self._offset(-self.width / 2, 0)

    @property
    def bl(self): return self._offset(-self.width / 2, -self.thickness / 2)

    @property
    def b(self):  return self._offset(0, -self.thickness / 2)

    @property
    def t(self):  return self._offset(0, self.thickness / 2)

    @property
    def br(self): return self._offset(self.width / 2, -self.thickness / 2)

    @property
    def r(self):  return self._offset(self.width / 2, 0)

    @property
    def tr(self): return self._offset(self.width / 2, self.thickness / 2)

    # --- Move / copy --------------------------------------------------------

    def moved_to(self, x: float, y: float) -> "PenNib":
        """Return a new nib at a new position."""
        return PenNib(self.width, self.thickness, self.angle, Vector(x, y))

    def outline(self) -> list[Vector]:
        """Return an array of vectors for the nib corners in order: tl, bl, br, tr."""
        return [self.tl, self.bl, self.br, self.tr]
