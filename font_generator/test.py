#!/usr/bin/env python3
from shapely.geometry import Polygon
from shapely.ops import unary_union
from pathlib import Path


def square_with_hole(outer_size: float, hole_size: float, cx: float, cy: float) -> Polygon:
    def square(cx, cy, size):
        half = size / 2
        return [
            (cx - half, cy - half),
            (cx + half, cy - half),
            (cx + half, cy + half),
            (cx - half, cy + half),
            (cx - half, cy - half),
        ]

    outer = square(cx, cy, outer_size)
    inner = square(cx, cy, hole_size)
    # return Polygon(shell=outer, holes=[inner])
    return outer, inner


def polygon_to_path_d(poly: Polygon) -> str:
    def ring_to_d(coords):
        pts = " ".join(f"{x:.5f},{y:.5f}" for x, y in coords)
        return f"M {pts} Z"

    parts = []
    parts.append(ring_to_d(poly.exterior.coords))
    for interior in poly.interiors:
        parts.append(ring_to_d(interior.coords))
    return " ".join(parts)


def write_svg(polygons, filename="combined.svg", margin=20, canvas_size=400):
    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_size}" height="{canvas_size}" viewBox="0 0 {canvas_size} {canvas_size}">')
    svg_parts.append(f'<rect width="100%" height="100%" fill="#f7f7f7"/>')
    svg_parts.append(f'<g transform="translate({margin},{margin})">')
    for poly in polygons:
        d = polygon_to_path_d(poly)
        svg_parts.append(f'<path d="{d}" fill="#000" fill-rule="evenodd" stroke="#000" stroke-width="1"/>')
    svg_parts.append("</g></svg>")
    Path(filename).write_text("\n".join(svg_parts), encoding="utf-8")
    print(f"Wrote {filename}")


if __name__ == "__main__":
    # # two identical squares-with-holes, same center so they overlap completely
    # outer = 200
    # hole = 80
    # cx = cy = 150  # center in canvas coordinates
    # a = square_with_hole(outer, hole, cx, cy)
    # b = square_with_hole(100, 10, 250, 250)  # identical; union will be same shape
    # combined = unary_union([a, b])  # boolean union
    # # combined may be a Polygon or MultiPolygon
    # polys = [combined] if combined.geom_type == "Polygon" else list(combined.geoms)
    o1, i1 = square_with_hole(10, 9, 20, 20)
    o2, i2 = square_with_hole(10, 8, 15, 15)
    s1 = Polygon(shell=o1, holes=[i1])
    s2 = Polygon(shell=o2, holes=[i2])
    # p1 = Polygon(shell=outer, holes=[inner])
    b1 = Polygon(shell=o1)
    b2 = Polygon(shell=o2)
    black = unary_union([s1, b2])  # boolean union
    w1 = Polygon(shell=i1)
    w2 = Polygon(shell=i2)
    white = unary_union([w1, w2])
    b_poly = [black] if black.geom_type == "Polygon" else list(black.geoms)
    w_poly = [white] if white.geom_type == "Polygon" else list(white.geoms)
    poly = black.difference(w2)
    polys = [poly] if poly.geom_type == "Polygon" else list(poly.geoms)

    write_svg(polys, filename="combined_squares.svg", margin=10, canvas_size=320)

