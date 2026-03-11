from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .vector import Vector


@dataclass(frozen=True)
class QuadraticBezier:
    p0: Vector
    p1: Vector
    p2: Vector

    def point_at(self, t: float) -> Vector:
        """Evaluate the Bezier curve at parameter t (0 to 1)."""
        mt = 1 - t
        return self.p0 * (mt * mt) + self.p1 * (2 * mt * t) + self.p2 * (t * t)

    def derivative_at(self, t: float) -> Vector:
        """Get the tangent (derivative) at parameter t."""
        mt = 1 - t
        return (self.p1 - self.p0) * (2 * mt) + (self.p2 - self.p1) * (2 * t)

    def normal_at(self, t: float) -> Vector:
        """Get the normal (perpendicular) at parameter t."""
        deriv = self.derivative_at(t)
        return Vector(-deriv.y, deriv.x).normalized()

    def split(self, t: float) -> Tuple[QuadraticBezier, QuadraticBezier]:
        """Split the curve at parameter t into two curves."""
        p01 = self.p0 * (1 - t) + self.p1 * t
        p12 = self.p1 * (1 - t) + self.p2 * t
        p012 = p01 * (1 - t) + p12 * t

        left = QuadraticBezier(self.p0, p01, p012)
        right = QuadraticBezier(p012, p12, self.p2)
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
