import math
from dataclasses import field

from .stroke_type import StrokeType
from .strokeable import Strokeable
from .vector import Vector


class CircleStroke(Strokeable):

    def __init__(self, centre: Vector,
                 radius: float,
                 from_angle: float = 0,
                 to_angle: float = 360,
                 offset: Vector =Vector.zero(),
                 stroke_type: StrokeType = StrokeType.Block,
                 num_samples: int = 20
                 ):
        super().__init__(stroke_type, num_samples)
        self.centre = centre
        self.radius = radius
        self.from_angle = from_angle
        self.to_angle = to_angle
        self.offset = offset

    def __post_init__(self):
        # Validate that angles are in range [0, 360]
        if not (0 <= self.from_angle <= 360):
            raise ValueError(f"from_angle must be in range [0, 360], got {self.from_angle}")
        if not (0 <= self.to_angle <= 360):
            raise ValueError(f"to_angle must be in range [0, 360], got {self.to_angle}")

        # Ensure to_angle > from_angle
        if self.to_angle < self.from_angle:
            raise ValueError(f"to_angle must be greater than or equal to from_angle, got from_angle={self.from_angle}, to_angle={self.to_angle}")

    def advance(self, pos: Vector) -> Vector:
        return pos + self.offset + self.centre + Vector(self.radius, 0).rotated(self.to_angle)

    def sample_points(self, num_samples: int = None) -> list[Vector]:
        # Use the base class's num_samples if not provided
        actual_num_samples = num_samples if num_samples is not None else self.num_samples

        # Ensure we have at least 2 points (start and end)
        if actual_num_samples < 2:
            actual_num_samples = 2

        # Handle case where from_angle equals to_angle
        if self.from_angle == self.to_angle:
            # Return the center point with offset
            return [self.centre + self.offset]

        # Calculate angle difference (handle 360 wraparound)
        angle_diff = self.to_angle - self.from_angle
        if angle_diff <= 0:
            angle_diff += 360

        # Handle case where from_angle equals to_angle after adjustment
        if angle_diff == 0:
            # Return the center point with offset
            return [self.centre + self.offset]

        # Generate points at evenly spaced angles
        points = []
        for i in range(actual_num_samples):
            # Calculate the current angle
            t = i / (actual_num_samples - 1) if actual_num_samples > 1 else 0
            current_angle = self.from_angle + t * angle_diff

            # Convert to radians
            rad = current_angle * math.pi / 180

            # Calculate the point on circle
            x = self.centre.x + self.offset.x + self.radius * math.cos(rad)
            y = self.centre.y + self.offset.y + self.radius * math.sin(rad)

            points.append(Vector(x, y))

        return points
