from enum import Enum


class NibType(Enum):
    Pen = "Pen"
    Circle = "Circle"

    def of(s: str) -> "NibType":
        for n in NibType:
            if n.value == s:
                return n
        raise ValueError(f"{s!r} is not a valid NibType")
