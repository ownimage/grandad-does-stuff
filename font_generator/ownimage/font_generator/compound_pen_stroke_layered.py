from dataclasses import dataclass

from .pen_nib import PenNib
from .vector import Vector


@dataclass(frozen=True)
class CompoundPenStrokeLayered:
    nib: PenNib
    points: list[Vector]
    step: float = 2.0   # distance between nib impressions

    def svg_paths(self) -> str:
        paths = []

        for i in range(len(self.points) - 1):
            p0 = self.points[i]
            p1 = self.points[i+1]

            direction = (p1 - p0).normalized()
            dist = (p1 - p0).length()

            steps = max(1, int(dist / self.step))

            for s in range(steps + 1):
                pos = p0 + direction * (s * self.step)
                n = self.nib.moved_to(pos.x, pos.y)

                pts = [n.tl, n.tr, n.br, n.bl]

                d = (
                    f"M {pts[0].x} {pts[0].y} "
                    + " ".join(f"L {pt.x} {pt.y}" for pt in pts[1:])
                    + " Z"
                )

                paths.append(f'<path d="{d}" fill="black" stroke="none" />')

        return "\n".join(paths)
