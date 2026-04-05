import math

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .nib import Nib
from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector import Vector


class CircleStroke(Strokeable):

    def __init__(self, centre: Vector | tuple[float, float],
                 radius: float,
                 from_angle: float = 0,
                 to_angle: float = 360,
                 offset: Vector = None,
                 x_factor: float = 1,
                 stroke_type: StrokeType = StrokeType.Block,
                 fp: FontParameters = None
                 ):
        num_samples = 20 if fp is None else fp.circle_samples
        super().__init__(stroke_type, num_samples)
        self.centre = Vector.of(centre)
        self.radius = radius
        self.from_angle = from_angle
        self.to_angle = to_angle
        self.x_factor = x_factor
        self.offset = offset if offset is not None else Vector(0, 0)


    @staticmethod
    def fill_height(
            top: float,
            bottom: float,
            from_angle: float = 0,
            to_angle: float = 360,
            x_factor: float = 1,
            stroke_type: StrokeType = StrokeType.Block,
            fp: FontParameters = None
    ) -> "CircleStroke":
        gs = GeometrySet()
        cs = CircleStroke(Vector.zero(), 1, from_angle, to_angle, fp=fp)
        cs.geometry(fp, Vector.zero(), 1, None, None, geom_set=gs)
        nib = Nib.from_font_parameters(fp)
        radius = (top - bottom - nib.height()) / (gs.bounding_box().height - nib.height())
        return CircleStroke((0, bottom + radius + nib.below()), radius, from_angle, to_angle, x_factor=x_factor, stroke_type=stroke_type, fp=fp)

    def __post_init__(self):
        # Validate that angles are in range [0, 360]
        if not (0 <= self.from_angle <= 360):
            raise ValueError(f"from_angle must be in range [0, 360], got {self.from_angle}")
        if not (0 <= self.to_angle <= 360):
            raise ValueError(f"to_angle must be in range [0, 360], got {self.to_angle}")

        # Ensure to_angle > from_angle
        if self.to_angle < self.from_angle:
            raise ValueError(f"to_angle must be greater than or equal to from_angle, got from_angle={self.from_angle}, to_angle={self.to_angle}")

    def point_at(self, t: float) -> Vector:
        angle_diff = self.to_angle - self.from_angle
        angle = self.from_angle + t * angle_diff
        rad = math.radians(angle)
        x = self.centre.x + self.offset.x + self.radius * math.cos(rad) * self.x_factor
        y = self.centre.y + self.offset.y + self.radius * math.sin(rad)
        return Vector(x, y)
