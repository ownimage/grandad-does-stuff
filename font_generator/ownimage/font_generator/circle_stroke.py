from dataclasses import dataclass, field
import math
from typing import TYPE_CHECKING

from shapely.geometry.multipoint import MultiPoint
from shapely.ops import unary_union

from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .pen_nib import PenNib
from .stroke import Stroke
from .strokeable import Strokeable
from .vector import Vector
from .vector_list import VectorList


@dataclass(frozen=True)
class CircleStroke(Strokeable):
    """Immutable circle stroke representation."""
    
    centre: Vector
    radius: float
    from_angle: float = 0
    to_angle: float = 360
    offset: Vector = field(default_factory=Vector.zero)

    def __post_init__(self):
        # Validate that angles are in range [0, 360]
        if not (0 <= self.from_angle <= 360):
            raise ValueError(f"from_angle must be in range [0, 360], got {self.from_angle}")
        if not (0 <= self.to_angle <= 360):
            raise ValueError(f"to_angle must be in range [0, 360], got {self.to_angle}")
            
        # Ensure to_angle > from_angle
        if self.to_angle < self.from_angle:
            raise ValueError(f"to_angle must be greater than or equal to from_angle, got from_angle={self.from_angle}, to_angle={self.to_angle}")

    def geometry(self, fp: FontParameters, start: Vector, scale: float, before: Strokeable, after: Strokeable, geom_set: GeometrySet) -> Vector:
        """
        Generate geometry by interpolating the nib along the curve
        and approximating it with short PenStroke segments.
        """

        def add_start_and_scale(pt: Vector) -> Vector:
            return Stroke.add_start_and_scale(pt, start, scale)

        points = self.sample_points(20) # TODO
        nib = PenNib.from_font_parameters(fp)
        geom_set.add_new_outline()
        outline = None

        for i in range(len(points) - 1):
            n1 = nib.at(points[i])
            n2 = nib.at(points[i + 1])
            p = [add_start_and_scale(p).xy() for p in n1.corners() + n2.corners()]
            h = MultiPoint(p).convex_hull
            outline = unary_union([outline, h])

        outline = VectorList.from_list_of_tuples(list(outline.exterior.coords))
        geom_set.replace_current_outline(outline)
        geom_set.add_new_outline()
        geom_set.add_new_hole()
        return start # TODO

    def advance(self, pos: Vector) -> Vector:
        return  pos + self.offset + self.centre + Vector(self.radius, 0).rotated(self.to_angle)

    def sample_points(self, num_samples: int = 20) -> list[Vector]:
        """Sample points along the circle stroke at evenly spaced angle values.
        
        Args:
            num_samples: Number of sample points to generate
            
        Returns:
            List of vectors representing points on the circle stroke
        """
        # Ensure we have at least 2 points (start and end)
        if num_samples < 2:
            num_samples = 2
            
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
        for i in range(num_samples):
            # Calculate the current angle
            t = i / (num_samples - 1) if num_samples > 1 else 0
            current_angle = self.from_angle + t * angle_diff
            
            # Convert to radians
            rad = current_angle * math.pi / 180
            
            # Calculate the point on circle
            x = self.centre.x + self.offset.x + self.radius * math.cos(rad)
            y = self.centre.y + self.offset.y + self.radius * math.sin(rad)
            
            points.append(Vector(x, y))
            
        return points