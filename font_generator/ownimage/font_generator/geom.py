from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

from shapely.geometry import Point


@dataclass
class Geom:
    class GeomType(Enum):
        Black = 1
        White = 2

    points: list[Point] = field(default_factory=list)
    geom_type: Geom.GeomType = GeomType.Black
