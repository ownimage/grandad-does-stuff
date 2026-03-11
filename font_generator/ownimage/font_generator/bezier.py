from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .vector import Vector


@dataclass(frozen=True)
class CubicBezier:
    p0: Vector
    p1: Vector
    p2: Vector
    p3: Vector

    def point_at(self, t: float) -> Vector:
        """Evaluate the Bezier curve at parameter t (0 to 1)."""
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        t2 = t * t
        t3 = t2 * t
        return (self.p0 * mt3 + 
                self.p1 * (3 * mt2 * t) + 
                self.p2 * (3 * mt * t2) + 
                self.p3 * t3)

    def derivative_at(self, t: float) -> Vector:
        """Get the tangent (derivative) at parameter t."""
        mt = 1 - t
        mt2 = mt * mt
        t2 = t * t
        return ((self.p1 - self.p0) * (3 * mt2) + 
                (self.p2 - self.p1) * (6 * mt * t) + 
                (self.p3 - self.p2) * (3 * t2))

    def normal_at(self, t: float) -> Vector:
        """Get the normal (perpendicular) at parameter t."""
        deriv = self.derivative_at(t)
        return Vector(-deriv.y, deriv.x).normalized()

    def split(self, t: float) -> Tuple[CubicBezier, CubicBezier]:
        """Split the curve at parameter t into two curves."""
        p01 = self.p0 * (1 - t) + self.p1 * t
        p12 = self.p1 * (1 - t) + self.p2 * t
        p23 = self.p2 * (1 - t) + self.p3 * t
        p012 = p01 * (1 - t) + p12 * t
        p123 = p12 * (1 - t) + p23 * t
        p0123 = p012 * (1 - t) + p123 * t

        left = CubicBezier(self.p0, p01, p012, p0123)
        right = CubicBezier(p0123, p123, p23, self.p3)
        return left, right

    def length(self, num_samples: int = 20) -> float:
        """Approximate the arc length of the curve."""
        total = 0.0
        prev = self.point_at(0)
        for i in range(1, num_samples + 1):
            t = i / num_samples
            curr = self.point_at(t)
            total += (curr - prev).length()
            prev = curr
        return total

    @staticmethod
    def from_three_points(p0: Vector, p1: Vector, p2: Vector) -> "CubicBezier":
        """Create a cubic bezier simulating a quadratic bezier from three points."""
        return CubicBezier(p0, p1, p1, p2)
