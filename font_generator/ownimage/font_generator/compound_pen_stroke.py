from dataclasses import dataclass

from .pen_nib import PenNib
from .pen_stroke import PenStroke
from .vector import Vector


@dataclass(frozen=True)
class CompoundPenStroke:
    nib: PenNib
    points: list[Vector]

    def svg_paths(self) -> str:
        """Return SVG for all stroke segments."""
        if len(self.points) < 2:
            return ""

        paths = []
        for i in range(len(self.points) - 1):
            start = self.nib.moved_to(self.points[i].x, self.points[i].y)
            end   = self.nib.moved_to(self.points[i+1].x, self.points[i+1].y)
            seg   = PenStroke(start, end)
            paths.append(seg.svg_path())

        return "\n".join(paths)