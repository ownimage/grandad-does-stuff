from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

from .vector import Vector


def _solve_cubic(a: float, b: float, c: float, d: float) -> List[float]:
    """Solve cubic equation ax³ + bx² + cx + d = 0 using Cardano's formula."""
    if abs(a) < 1e-10:
        if abs(b) < 1e-10:
            if abs(c) < 1e-10:
                return []
            return [-d / c]
        disc = c * c - 4 * b * d
        if disc < 0:
            return []
        sqrt_disc = math.sqrt(disc)
        return [(-c + sqrt_disc) / (2 * b), (-c - sqrt_disc) / (2 * b)]

    b /= a
    c /= a
    d /= a

    q = (3 * c - b * b) / 9
    r = (9 * b * c - 27 * d - 2 * b * b * b) / 54
    disc = q * q * q + r * r

    roots: List[float] = []

    if disc > 1e-10:
        s = r + math.sqrt(disc)
        t = r - math.sqrt(disc)
        s = math.copysign(abs(s) ** (1/3), s)
        t = math.copysign(abs(t) ** (1/3), t)
        root = -b / 3 + s + t
        roots.append(root)
    elif abs(disc) < 1e-10:
        if abs(r) < 1e-10:
            roots.append(-b / 3)
        else:
            s = math.copysign(abs(r) ** (1/3), r)
            root = -b / 3 + 2 * s
            roots.append(root)
            roots.append(-b / 3 - s)
    else:
        theta = math.acos(r / math.sqrt(-q * q * q))
        sqrt_minus_q = math.sqrt(-q)
        roots.append(-b / 3 + 2 * sqrt_minus_q * math.cos(theta / 3))
        roots.append(-b / 3 + 2 * sqrt_minus_q * math.cos((theta + 2 * math.pi) / 3))
        roots.append(-b / 3 + 2 * sqrt_minus_q * math.cos((theta + 4 * math.pi) / 3))

    return [r for r in roots if 0 <= r <= 1]


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

    def closet_t_to(self, target: Vector) -> float:
        """Find the parameter t (0 to 1) on the curve closest to the target point."""
        candidates = [0.0, 1.0]

        cp0 = self.p0 - target
        cp1 = self.p1 - target
        cp2 = self.p2 - target
        cp3 = self.p3 - target

        def dot(a: Vector, b: Vector) -> float:
            return a.x * b.x + a.y * b.y

        a = dot(cp3, cp3) - 3 * dot(cp2, cp2) + 3 * dot(cp1, cp1) - dot(cp0, cp0)
        b = 6 * dot(cp2, cp2) - 12 * dot(cp1, cp1) + 6 * dot(cp0, cp0)
        c = 3 * dot(cp1, cp1) - 6 * dot(cp0, cp0)
        d = dot(cp0, cp0)

        roots = _solve_cubic(a, b, c, d)
        candidates.extend(roots)

        best_t = 0.0
        best_dist = float('inf')

        for t in candidates:
            if 0 <= t <= 1:
                point = self.point_at(t)
                dist = (point - target).length()
                if dist < best_dist:
                    best_dist = dist
                    best_t = t

        return best_t

    def distance_to(self, target: Vector) -> float:
        """Calculate the minimum distance from a point to this bezier curve."""
        closest_t = self.closet_t_to(target)
        closest_point = self.point_at(closest_t)
        return (closest_point - target).length()

    def sample_points(self, num_samples: int = 20) -> List[Vector]:
        """Sample points along the curve at evenly spaced t values."""
        points = []
        for i in range(num_samples):
            t = i / (num_samples - 1)
            points.append(self.point_at(t))
        return points

    def move_to(self, start: Vector) -> "CubicBezier":
        """Move the bezier curve so that its starting point is at the given vector.
        
        This creates a new bezier where all control points are offset by the 
        vector delta = start - p0.
        
        Args:
            start: The new starting position for the bezier curve
            
        Returns:
            A new CubicBezier with the same shape but starting at the given position
        """
        delta = start - self.p0
        return CubicBezier(
            self.p0 - delta,
            self.p1 - delta,
            self.p2 - delta,
            self.p3 - delta
        )

