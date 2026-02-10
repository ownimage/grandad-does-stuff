from shapely.geometry import Point


class GeometrySet:
    def __init__(self):
        self.outlines: list[list[Point]] = [[]]
        self.holes: list[list[Point]] = [[]]
        self.graffiti: list[list[Point]] = [[]]

    def get_current_outline(self) -> list[Point]:
        return self.outlines[-1]

    def add_new_outline(self, outline=None):
        if outline is None:
            outline = []
        self.outlines.append(outline)

    def replace_current_outline(self, outline: list[Point]):
        self.outlines.pop()
        self.add_new_outline(outline)

    def svg(self) -> str:
        svg = ""
        colour = "black"
        for outline in self.outlines:
            if len(outline) == 0:
                continue
            p0 = outline[0]
            svg += f"""<path d ="M{p0.x} {p0.y} """
            for p in outline[1:]:
                svg += f"""L{p.x} {p.y} """
            svg += f"""Z" fill="{colour}" stroke="black" stroke-width=".5" />\n"""
        return svg