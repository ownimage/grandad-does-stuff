import random
from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton
)

from font_generator.ownimage.font_generator.compound_pen_outline import CompoundPenOutline
from font_generator.ownimage.font_generator.compound_pen_outline_ring import CompoundPenOutlineRing
from font_generator.ownimage.font_generator.compound_pen_outline_unified import CompoundPenOutlineRingUnified
from font_generator.ownimage.font_generator.compound_pen_stroke import CompoundPenStroke
from font_generator.ownimage.font_generator.compound_pen_stroke_layered import CompoundPenStrokeLayered
from font_generator.ownimage.font_generator.pen_nib import PenNib
from font_generator.ownimage.font_generator.vector import Vector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compound Pen Outline Demo")

        layout = QVBoxLayout()

        # SVG pane
        self.svg = QSvgWidget()
        self.svg.setFixedSize(600, 400)
        layout.addWidget(self.svg)

        # Sliders
        self.width  = self.make_slider(layout, 5, 200, 60, "Nib Width")
        self.thick  = self.make_slider(layout, 2, 100, 20, "Nib Thickness")
        self.angle  = self.make_slider(layout, 0, 180, 45, "Angle")

        # Randomise button
        btn = QPushButton("Randomise Points")
        btn.clicked.connect(self.randomise_points)
        layout.addWidget(btn)

        # Initial random points
        self.randomise_points()

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

    def randomise_points(self):
        self.points = [
            Vector(random.randint(50, 550), random.randint(50, 350))
            for _ in range(4)
        ]
        self.update_svg()

    def update_svg(self):
        nib = PenNib(
            width=self.width.value(),
            thickness=self.thick.value(),
            angle=self.angle.value(),
            pos=Vector(0, 0)
        )

        ring = CompoundPenOutlineRing(nib, self.points, edge=nib.thickness)


        W, H = 600, 400

        svg = f"""
<svg width="{W}" height="{H}"
     viewBox="0 0 {W} {H}"
     xmlns="http://www.w3.org/2000/svg">

    <rect x="0" y="0" width="{W}" height="{H}" fill="white" />

    <!-- Debug: show points -->


    {ring.svg_paths()}
    
    {"".join(f'<circle cx="{p.x}" cy="{p.y}" r="10" fill="red" />' for p in self.points)}

</svg>
"""



        print(svg)
        self.svg.load(bytearray(svg, encoding="utf-8"))


# ---------------------------------------------------------
#  Run the app
# ---------------------------------------------------------
if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()
