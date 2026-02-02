import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QCheckBox, QSlider, QLabel
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt
from vector2d import Vector2D

from .blackletter import Blackletter


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dynamic SVG Example")

        self.checkbox = QCheckBox()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(10, 70)
        self.slider.setValue(40)

        self.svg_widget = QSvgWidget()
        self.svg_widget.setFixedSize(150, 150)

        checkbox_row = QHBoxLayout()
        checkbox_row.addWidget(QLabel("Filled:"))
        checkbox_row.addWidget(self.checkbox)
        checkbox_row.addStretch()

        slider_row = QHBoxLayout()
        slider_row.addWidget(QLabel("Radius:"))
        slider_row.addWidget(self.slider)

        self.update_svg()

        self.checkbox.stateChanged.connect(self.update_svg)
        self.slider.valueChanged.connect(self.update_svg)

        layout = QVBoxLayout()
        layout.addWidget(self.svg_widget)
        layout.addLayout(checkbox_row)
        layout.addLayout(slider_row)
        self.setLayout(layout)

    def update_svg(self):
        radius = float(self.slider.value())
        svg_data = self.make_svg(radius)
        self.svg_widget.load(bytearray(svg_data, encoding="utf-8"))

    def make_svg(self, scale: float) -> str:
        width = 500
        height = 150

        blackletter = Blackletter(.5, 0, 3, 7)

        return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {height} {height}" 
        xmlns="http://www.w3.org/2000/svg">
    
        <rect x="0" y="0" width="{width}" height="{height}" fill="white"/>
        <g transform="translate(0, {height}) scale(1, -1)">
            {blackletter.svg(Vector2D(1,0), scale)}
        </g>
    </svg>
    """


