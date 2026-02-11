from .vector import Vector


class GeometrySet:
    def __init__(self):
        self.outlines: list[list[Vector]] = [[]]
        self.holes: list[list[Vector]] = [[]]
        self.graffiti: list[list[Vector]] = [[]]

    def get_current_outline(self) -> list[Vector]:
        return self.outlines[-1]

    def add_new_outline(self, outline=None):
        if outline is None:
            outline = []
        self.outlines.append(outline)

    def replace_current_outline(self, outline: list[Vector]):
        self.outlines.pop()
        self.add_new_outline(outline)

    def get_current_hole(self) -> list[Vector]:
        return self.holes[-1]

    def add_new_hole(self, hole=None):
        if hole is None:
            hole = []
        self.holes.append(hole)

    def replace_current_hole(self, hole: list[Vector]):
        self.holes.pop()
        self.add_new_hole(hole)

    def svg(self, filled: bool) -> str:
        svg = self.svg_writer(self.outlines, "black")

        if not filled:
            svg += self.svg_writer(self.holes, "white")
        return svg

    def svg_writer(self, paths: list[list[Vector]], colour: str):
        svg = ""
        for path in paths:
            path = [p for p in path if p is not None]
            if len(path) == 0:
                continue
            p0 = path[0]
            if not isinstance(p0, Vector):
                raise ValueError("Path must be a list of points")
            if len(path) == 1:
                continue
            svg += f"""<path d ="M{p0.x} {p0.y} """
            for p in path[1:]:
                svg += f"""L{p.x} {p.y} """
            svg += f"""Z" fill="{colour}" />\n"""
        return svg
