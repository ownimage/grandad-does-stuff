from __future__ import annotations

from dataclasses import replace
from typing import List

from .bezier_stroke import BezierStroke
from .bounding_box import BoundingBox
from .circle_stroke import CircleStroke
from .compound_stroke import CompoundStroke
from .font_parameters import FontParameters
from .geometry_set import GeometrySet
from .nib import Nib
from .pen_nib import PenNib
from .stroke import Stroke, Strokeable
from .vector import Vector


class Mark:
    def __init__(
            self,
            strokes: List[Strokeable] | Strokeable,
            vec: Vector = None,
            x: float = None,
            y: float = None,
    ):
        if vec is not None:
            if x is not None or y is not None:
                raise ValueError("Cannot specify vec and x or y")
            self.vec = vec
        elif x is not None or y is not None:
            self.vec = Vector(x or 0, y or 0)
        else:
            self.vec = Vector(0, 0)

        # Normalise strokes to a flat list of Strokeable
        if isinstance(strokes, Strokeable):
            # Single stroke (including CompoundStroke if it subclasses Strokeable)
            if isinstance(strokes, CompoundStroke):
                self.strokes = strokes.strokes  # assuming CompoundStroke is iterable
            else:
                self.strokes = [strokes]
        else:
            # Already a list/iterable of Strokeable
            self.strokes = list(strokes)

    def __add__(self, v) -> Mark:
        return Mark(self.strokes, self.vec + v)

    def __sub__(self, v) -> Mark:
        return Mark(self.strokes, self.vec - v)

    def left_by(self, amount: float):
        return Mark(self.strokes, Vector(self.vec.x - amount, self.vec.y))

    def right_by(self, amount: float):
        return Mark(self.strokes, Vector(self.vec.x + amount, self.vec.y))

    def up_by(self, amount: float):
        return Mark(self.strokes, Vector(self.vec.x, self.vec.y + amount))

    def down_by(self, amount: float):
        return Mark(self.strokes, Vector(self.vec.x, self.vec.y - amount))

    def bottom_at(self, target: float, fp: FontParameters, start: Vector = Vector(0, 0), scale: float = 1.0):
        current = self.bounding_box(fp, start, scale).bottom
        shift = target - current
        return self.up_by(shift)

    def top_at(self, target: float, fp: FontParameters, start: Vector = Vector(0, 0), scale: float = 1.0):
        current = self.bounding_box(fp, start, scale).top
        shift = target - current
        return self.up_by(shift)

    def top_at_bezier(self, fp: FontParameters, mark: Mark, index: int = 0, start: Vector = Vector(0, 0), scale: float = 1.0):
        current = self.top(fp, start, scale)
        target = mark.bezier_y_at_x(index, self.vec.x)
        shift = target - current
        return self.up_by(shift)

    def start_at_bezier(self, fp: FontParameters, mark: Mark, index: int = 0, start: Vector = Vector(0, 0), scale: float = 1.0):
        beziers = [s for s in mark.strokes if isinstance(s, BezierStroke)]
        bezier = beziers[0]
        current = self.vec.y
        target = mark.vec.y + bezier.y_at_x(self.vec.x)[index]
        shift = target - current
        return self.up_by(shift)

    def left_at(self, target: float, fp: FontParameters, start: Vector = Vector(0, 0), scale: float = 1.0):
        current = self.bounding_box(fp, start, scale).left
        shift = target - current
        return self.right_by(shift)

    def centre_x_at(self, target: float, fp: FontParameters, start: Vector = Vector(0, 0), scale: float = 1.0):
        current = self.bounding_box(fp, start, scale).cx
        shift = target - current
        return self.right_by(shift)

    def right_at(self, target: float, fp: FontParameters, start: Vector = Vector(0, 0), scale: float = 1.0):
        current = self.bounding_box(fp, start, scale).right
        shift = target - current
        return self.right_by(shift)

    def geometry(self, start: Vector, fp: FontParameters, scale: float = 1) -> GeometrySet:
        nib = PenNib.from_font_parameters(fp)
        start = start + self.vec
        geom_set = GeometrySet()

        for idx, (start_offset, width) in enumerate(fp.pen_stroke):
            fpt = replace(fp, pen_width=width)
            current_pos = start

            for i in range(len(self.strokes)):
                curr_item = self.strokes[i]
                prev_item = self.strokes[i - 1] if i > 0 else None
                next_item = self.strokes[i + 1] if i < len(self.strokes) - 1 else None

                if isinstance(curr_item, Strokeable):
                    offset_pos = current_pos + nib.direction * (-0.5 * fp.pen_width + start_offset + 0.5 * width)
                    curr_item.geometry(fpt, offset_pos, scale, prev_item, next_item, geom_set)
                elif idx == 0:
                    curr_item.geometry(fp, current_pos, scale, prev_item, next_item, geom_set)

                current_pos = curr_item.advance(current_pos)

        return geom_set

    def stroke_bounding_box(self, index: int, fp: FontParameters, start: Vector = Vector(0, 0), scale: float = 1.0) -> BoundingBox:
        geom_set = GeometrySet()
        start = start + self.stroke_start(index)

        curr_item = self.strokes[index]
        prev_item = self.strokes[index - 1] if index > 0 else None
        next_item = self.strokes[index + 1] if index < len(self.strokes) - 1 else None
        curr_item.geometry(fp, start, scale, prev_item, next_item, geom_set)
        return geom_set.bounding_box()

    def bounding_box(self, fp: FontParameters, start: Vector = Vector(0, 0), scale: float = 1.0) -> BoundingBox:
        geom = self.geometry(start, fp, scale)
        return geom.bounding_box()  # -> (bl, tr)

    def extend_downstroke_to_set_bottom_at(self, stroke, bottom, fp):
        return self.with_stroke(stroke, lambda s: s.extend(self.bounding_box(fp).bottom - bottom))

    def set_stroke_end(self, i: int, end: Vector):
        stroke = self.strokes[i]
        if isinstance(stroke, BezierStroke):
            return self.with_stroke(i, lambda s, vec=self.vec: replace(s, bezier=replace(s.bezier, p3=end - vec)))
        raise TypeError(f"Not implemented for {stroke.__class__.__name__}")

    def set_stroke_start(self, i: int, start: Vector):
        stroke = self.strokes[i]
        if isinstance(stroke, BezierStroke):
            return self.with_stroke(i, lambda s, vec=self.vec: replace(s, bezier=replace(s.bezier, p0=start - vec)))
        raise TypeError(f"Not implemented for {stroke.__class__.__name__}")

    def extend_downstroke_to_bezier(self, stroke, fp: FontParameters, mark: Mark, bezier_index: int = 0):
        current_end = self.stroke_end(stroke)
        target = mark.bezier_y_at_x(bezier_index, current_end.x)
        return self.with_stroke(stroke, lambda s: s.extend(current_end.y - target))

    def bezier_y_at_x(self, i: int, x: float, crossing: int = 0) -> float:
        beziers = [s for s in self.strokes if isinstance(s, BezierStroke)]
        bezier = beziers[i]
        return self.vec.y + bezier.y_at_x(x)[crossing]

    def extend_rightstroke_to_set_right_at(self, stroke, right, fp):
        delta = right - self.bounding_box(fp).right
        return self.with_stroke(stroke, lambda s: s.extend(Vector(delta, 0)))

    def extend_stroke_backwards_to_x(self, stroke, x, fp):
        current_x = self.stroke_tl(stroke, fp).x
        delta_x = current_x - x
        delta_y = delta_x * self.strokes[stroke].vec.y / self.strokes[stroke].vec.x
        delta = Vector(delta_x, delta_y)

        if stroke == 0:
            new_strokes = list(self.strokes)
            new_strokes[stroke] = self.strokes[stroke].extend(delta)
            return Mark(new_strokes, self.vec - delta)
        else:
            return self.with_stroke(stroke, lambda s: s.extend(delta))

    def svg(self, fp: FontParameters, start: Vector, scale: float) -> str:
        return self.geometry(start, fp, scale).svg(fp.filled) + "\n"

    def birdfont_path(self, fp: FontParameters, scale: float):
        start = self.vec
        paths = []
        for stroke in self.strokes:
            start, stroke_paths = stroke.birdfont_path(start, fp, scale)
            paths += stroke_paths

        return paths

    def with_stroke(self, i: int, f) -> Mark:
        new_strokes = list(self.strokes)
        new_strokes[i] = f(new_strokes[i])
        return Mark(new_strokes, self.vec)

    def stroke_start(self, i: int) -> Vector:
        start = self.vec
        for s in self.strokes[:i]:
            start = s.advance(start)
        return start

    def stroke_end(self, i: int) -> Vector:
        start = self.stroke_start(i)
        return self.strokes[i].advance(start)

    def stroke_bl(self, i: int, fp: FontParameters) -> Vector:
        start = self.stroke_start(i)
        return start + self.strokes[i].bl(fp)

    def stroke_tr(self, i: int, fp: FontParameters) -> Vector:
        start = self.stroke_start(i)
        return start + self.strokes[i].tr(fp)

    def stroke_br(self, i: int, fp: FontParameters) -> Vector:
        start = self.stroke_start(i)
        return start + self.strokes[i].br(fp)

    def stroke_tl(self, i: int, fp: FontParameters) -> Vector:
        start = self.stroke_start(i)
        return start + self.strokes[i].tl(fp)
