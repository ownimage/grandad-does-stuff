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
    
    @property
    def tl(self) -> Vector:
        """Top-left corner vector."""
        return Vector(self.left, self.top)
    
    @property
    def bl(self) -> Vector:
        """Bottom-left corner vector."""
        return Vector(self.left, self.bottom)
    
    @property
    def tr(self) -> Vector:
        """Top-right corner vector."""
        return Vector(self.right, self.top)
    
    @property
    def br(self) -> Vector:
        """Bottom-right corner vector."""
        return Vector(self.right, self.bottom)
    
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
        return Vector((self.left + self.right) / 2, (self.top + self.bottom) / 2)
    
    @property
    def cx(self) -> float:
        """X coordinate of the center."""
        return self.center.x
    
    @property
    def cy(self) -> float:
        """Y coordinate of the center."""
        return self.center.y