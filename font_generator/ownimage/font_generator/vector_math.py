import math

from .vector import Vector

class VectorMath:
    """Utility methods for simple vector-style operations on Shapely Points."""

    @staticmethod
    def add_points(a: Vector, b: Vector) -> Vector:
        """Return a new Vector equal to a + b."""
        return Vector(a.x + b.x, a.y + b.y)

    @staticmethod
    def subtract_points(a: Vector, b: Vector) -> Vector:
        """Return a new Vector equal to a - b."""
        return Vector(a.x - b.x, a.y - b.y)

    @staticmethod
    def scale_point(p: Vector, factor: float) -> Vector:
        """Return a new Vector equal to p * factor."""
        return Vector(p.x * factor, p.y * factor)

    @staticmethod
    def normalize(p: Vector) -> Vector:
        """Return a unit-length version of the Vector treated as a vector."""
        length = (p.x ** 2 + p.y ** 2) ** 0.5
        if length == 0:
            return Vector(0, 0)
        return Vector(p.x / length, p.y / length)

    @staticmethod
    def line_intersection(p1: Vector, p2: Vector, p3: Vector, p4: Vector) -> Vector:
        """Return instsection of line between p1, p2 and p3, p4"""
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y
        x4, y4 = p4.x, p4.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None  # parallel or coincident

        det1 = x1 * y2 - y1 * x2
        det2 = x3 * y4 - y3 * x4

        x = (det1 * (x3 - x4) - (x1 - x2) * det2) / den
        y = (det1 * (y3 - y4) - (y1 - y2) * det2) / den

        return Vector(x, y)

    @staticmethod
    def left_normal(v):
        # Rotate 90° CCW and normalise
        length = math.hypot(v.x, v.y)
        return type(v)(-v.y / length, v.x / length)

    @staticmethod
    def line_intersection2(p1, v1, p2, v2):
        # Solve p1 + t*v1 = p2 + u*v2
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        vx1, vy1 = v1.x, v1.y
        vx2, vy2 = v2.x, v2.y

        den = vx1 * (-vy2) - vy1 * (-vx2)
        if den == 0:
            return None  # parallel

        dx = x2 - x1
        dy = y2 - y1

        t = (dx * (-vy2) - dy * (-vx2)) / den

        return type(p1)(x1 + t * vx1, y1 + t * vy1)

    @staticmethod
    def offset_intersection(p, v1, v2, t):
        n1 = VectorMath.left_normal(v1)
        n2 = VectorMath.left_normal(v2)

        p1 = type(p)(p.x + n1.x * t, p.y + n1.y * t)
        p2 = type(p)(p.x + n2.x * t, p.y + n2.y * t)

        return VectorMath.line_intersection2(p1, v1, p2, v2)
