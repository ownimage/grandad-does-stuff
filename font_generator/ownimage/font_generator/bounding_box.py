from dataclasses import dataclass, field
from typing import Union

from .vector import Vector


@dataclass(frozen=True)
class BoundingBox:
    """Immutable bounding box represented by bottom_left and top_right vectors."""
    
    bottom_left: Vector
    top_right: Vector
    
    def __post_init__(self):
        # Validate that bottom_left is actually bottom left and top_right is actually top right
        if self.bottom_left.x > self.top_right.x:
            raise ValueError("bottom_left.x must be <= top_right.x")
        if self.bottom_left.y > self.top_right.y:
            raise ValueError("bottom_left.y must be <= top_right.y")
    
    @classmethod
    def from_coords(cls, left: float, bottom: float, right: float, top: float) -> "BoundingBox":
        """Create BoundingBox from 4 float coordinates."""
        return cls(Vector(left, bottom), Vector(right, top))
    
    def __sub__(self, other: "BoundingBox") -> "BoundingBox":
        """Calculate difference of two bounding boxes."""
        # The difference is defined by the difference of coordinates
        new_bottom_left = Vector(
            self.bottom_left.x - other.bottom_left.x,
            self.bottom_left.y - other.bottom_left.y
        )
        new_top_right = Vector(
            self.top_right.x - other.top_right.x,
            self.top_right.y - other.top_right.y
        )
        return BoundingBox(new_bottom_left, new_top_right)
    
    @property
    def tl(self) -> Vector:
        """Top-left corner vector."""
        return Vector(self.bottom_left.x, self.top_right.y)
    
    @property
    def bl(self) -> Vector:
        """Bottom-left corner vector."""
        return self.bottom_left
    
    @property
    def tr(self) -> Vector:
        """Top-right corner vector."""
        return self.top_right
    
    @property
    def br(self) -> Vector:
        """Bottom-right corner vector."""
        return Vector(self.top_right.x, self.bottom_left.y)
    
    @property
    def left(self) -> float:
        """Left coordinate."""
        return self.bottom_left.x
    
    @property
    def right(self) -> float:
        """Right coordinate."""
        return self.top_right.x
    
    @property
    def top(self) -> float:
        """Top coordinate."""
        return self.top_right.y
    
    @property
    def bottom(self) -> float:
        """Bottom coordinate."""
        return self.bottom_left.y
    
    @property
    def center(self) -> Vector:
        """Center point as a vector."""
        return Vector(
            (self.bottom_left.x + self.top_right.x) / 2,
            (self.bottom_left.y + self.top_right.y) / 2
        )
    
    @property
    def cx(self) -> float:
        """X coordinate of the center."""
        return self.center.x
    
    @property
    def cy(self) -> float:
        """Y coordinate of the center."""
        return self.center.y