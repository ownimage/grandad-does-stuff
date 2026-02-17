from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QSlider
)
from dataclasses import dataclass, field
from math import sin, cos, radians

from font_generator.ownimage.font_generator.pen_nib import PenNib
from font_generator.ownimage.font_generator.pen_stroke import PenStroke
from font_generator.ownimage.font_generator.vector import Vector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pen Stroke Demo")

        layout = QVBoxLayout()

        # SVG pane
        self.svg = QSvgWidget()
        self.svg.setFixedSize(600, 400)
        layout.addWidget(self.svg)

        # Sliders
        self.width = self.make_slider(layout, 5, 200, 60, "Nib Width")
        self.thick = self.make_slider(layout, 2, 100, 20, "Nib Thickness")
        self.angle = self.make_slider(layout, 0, 180, 45, "Angle")
        self.xpos  = self.make_slider(layout, 0, 400, 200, "X Position")
        self.ypos  = self.make_slider(layout, 0, 300, 150, "Y Position")

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.update_svg()

    def make_slider(self, layout, mn, mx, val, name):
        row = QHBoxLayout()
        label = QLabel(name)
        slider = QSlider(Qt.Horizontal)
        slider.setRange(mn, mx)
        slider.setValue(val)
        slider.valueChanged.connect(self.update_svg)

        row.addWidget(label)
        row.addWidget(slider)
        layout.addLayout(row)
        return slider

    def update_svg(self):
        # Start nib fixed at (100, 200)
        start = PenNib(
            width=self.width.value(),
            thickness=self.thick.value(),
            angle=self.angle.value(),
            pos=Vector(100, 200)
        )

        # End nib controlled by sliders
        end = start.moved_to(self.xpos.value(), self.ypos.value())

        stroke = PenStroke(start, end)

        W, H = 600, 400

        svg = f"""
    <svg width="{W}" height="{H}"
         viewBox="0 0 {W} {H}"
         xmlns="http://www.w3.org/2000/svg">

        <rect x="0" y="0" width="{W}" height="{H}" fill="white" />

        {stroke.svg_path()}
    </svg>
    """

        print(svg)  # so you can inspect the exact SVG output

        self.svg.load(bytearray(svg, encoding="utf-8"))


# ---------------------------------------------------------
#  Run the app
# ---------------------------------------------------------
if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()
