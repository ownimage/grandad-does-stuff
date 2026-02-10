from typing import Optional
from svgpathtools import CubicBezier, wsvg, Path
import math
import cmath

def _unit_normal(p1: complex, p2: complex) -> complex:
    """Unit normal (rotate +90°) for the vector p2-p1."""
    v = p2 - p1
    nx = complex(-v.imag, v.real)
    norm = abs(nx)
    return nx / norm if norm != 0 else 0+0j

def _line_from_segment(p1: complex, p2: complex, offset: float) -> tuple[complex, complex]:
    """
    Return (point_on_shifted_line, direction) for the line through segment p1->p2
    shifted outward by offset along its normal.
    """
    dir_vec = p2 - p1
    n = _unit_normal(p1, p2)
    return (p1 + n * offset, dir_vec)

def _intersect_lines(pA: complex, dA: complex, pB: complex, dB: complex) -> Optional[complex]:
    """
    Intersection of two infinite lines: pA + t*dA and pB + u*dB.
    Returns None if parallel (or nearly).
    """
    # Solve pA + t*dA = pB + u*dB  =>  t*dA - u*dB = pB - pA
    # Use complex algebra: treat as 2x2 real system
    ax, ay = dA.real, dA.imag
    bx, by = dB.real, dB.imag
    rx, ry = (pB - pA).real, (pB - pA).imag
    det = ax * (-by) - ay * (-bx)  # det of [[ax, -bx],[ay, -by]] = ax*(-by) - ay*(-bx)
    if abs(det) < 1e-12:
        return None
    t = (rx * (-by) - ry * (-bx)) / det
    return pA + dA * t

def tiller_hanson_offset(cubic: CubicBezier, d: float) -> CubicBezier:
    """
    Compute a Tiller–Hanson approximate offset of a cubic Bezier.
    Returns a new CubicBezier approximating the offset at distance d.
    """
    P0, P1, P2, P3 = cubic.start, cubic.control1, cubic.control2, cubic.end

    # Build shifted lines for control-polygon edges
    pA, dA = _line_from_segment(P0, P1, d)
    pB, dB = _line_from_segment(P1, P2, d)
    pC, dC = _line_from_segment(P2, P3, d)

    # Intersect adjacent shifted lines to get new interior control points
    Q1 = _intersect_lines(pA, dA, pB, dB)
    Q2 = _intersect_lines(pB, dB, pC, dC)

    # Fallbacks if intersections fail (parallel edges): shift original control points
    if Q1 is None:
        Q1 = P1 + _unit_normal(P0, P1) * d
    if Q2 is None:
        Q2 = P2 + _unit_normal(P2, P3) * d

    # Shift endpoints by their adjacent edge normals (use edge normals)
    N0 = _unit_normal(P0, P1)
    N3 = _unit_normal(P2, P3)
    Q0 = P0 + N0 * d
    Q3 = P3 + N3 * d

    return CubicBezier(Q0, Q1, Q2, Q3)

def original():
    # points and directions as complex numbers: x + y*1j
    A = 200 + 400j            # start point (A)
    C = 600 + 200j         # end point (C)
    dirA = 1 + 0j         # start direction (B) (can be unit)
    dirC = 1 - 1j        # end direction (D) (can be unit)

    # choose tangent lengths (scales)
    scaleA = 1 * abs(C - A)
    scaleC = 1 * abs(C - A)

    T_A = dirA / abs(dirA) * scaleA   # normalized * length
    T_C = dirC / abs(dirC) * scaleC

    P0 = A
    P1 = P0 + T_A / 3
    P3 = C
    P2 = P3 - T_C / 3

    curve = CubicBezier(P0, P1, P2, P3)
    p = curve.point(0.5)
    n = curve.normal(0.5)
    p2 = p + n * 50
    return curve

def parallel(p):
    P0 = 200 + 350j  # E
    P3 = 565 + 165j# G
    F = p # 300 + 60j  # point to pass through (F)
    t = 0.5

    # compute RHS for t=0.5
    rhs = (8 / 3) * F - (1 / 3) * (P0 + P3)

    # choose P1 by heuristic (alpha controls shape)
    alpha = 0.5
    P1 = P0 + alpha * (F - P0)
    P2 = rhs - P1

    curve = CubicBezier(P0, P1, P2, P3)
    return Path(curve)

o = original()
offset_curve = tiller_hanson_offset(o, d=5.0)
wsvg([Path(o), offset_curve], 'gr', filename='offset_curves.svg')
