from shapely.geometry import Point

class VectorMath:
    """Utility methods for simple vector-style operations on Shapely Points."""

    @staticmethod
    def add_points(a: Point, b: Point) -> Point:
        """Return a new Point equal to a + b."""
        return Point(a.x + b.x, a.y + b.y)

    @staticmethod
    def subtract_points(a: Point, b: Point) -> Point:
        """Return a new Point equal to a - b."""
        return Point(a.x - b.x, a.y - b.y)

    @staticmethod
    def scale_point(p: Point, factor: float) -> Point:
        """Return a new Point equal to p * factor."""
        return Point(p.x * factor, p.y * factor)

    @staticmethod
    def normalize(p: Point) -> Point:
        """Return a unit-length version of the point treated as a vector."""
        length = (p.x**2 + p.y**2) ** 0.5
        if length == 0:
            return Point(0, 0)
        return Point(p.x / length, p.y / length)
