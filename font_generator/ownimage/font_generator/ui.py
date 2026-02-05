import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QCheckBox, QSlider, QLabel, QMainWindow, QWidget, QFileDialog
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt
from shapely.geometry import Point

from .birdfont_reader import BirdfontReader
from .blackletter import Blackletter
from .font_parameters import FontParameters


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.create_menu()

        self.setWindowTitle("Font Generator")

        self.filled = QCheckBox()
        self.scale = QSlider(Qt.Horizontal)
        self.scale.setRange(10, 400)
        self.scale.setValue(40)

        self.svg_width = 2000
        self.svg_height = 300
        self.svg_widget = QSvgWidget()
        self.svg_widget.setFixedSize(self.svg_width, self.svg_height)

        checkbox_row = QHBoxLayout()
        checkbox_row.addWidget(QLabel("Filled:"))
        checkbox_row.addWidget(self.filled)
        checkbox_row.addStretch()

        slider_row = QHBoxLayout()
        slider_row.addWidget(QLabel("Scale:"))
        slider_row.addWidget(self.scale)

        self.update_svg()

        self.filled.stateChanged.connect(self.update_svg)
        self.scale.valueChanged.connect(self.update_svg)

        layout = QVBoxLayout()
        layout.addWidget(self.svg_widget)
        layout.addLayout(checkbox_row)
        layout.addLayout(slider_row)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.blackletter = Blackletter(self.get_fontParameters())

    def update_svg(self):
        radius = float(self.scale.value())
        svg_data = self.make_svg(radius)
        self.svg_widget.load(bytearray(svg_data, encoding="utf-8"))

    def get_fontParameters(self):
        return FontParameters(0.5, self.filled.isChecked(), 0, 3, 7)

    def make_svg(self, scale: float) -> str:
        self.blackletter = Blackletter(self.get_fontParameters())

        return f"""
    <svg width="{self.svg_width}" height="{self.svg_height}" viewBox="0 0 {self.svg_width} {self.svg_height}" 
        xmlns="http://www.w3.org/2000/svg">
    
        <rect x="0" y="0" width="{self.svg_width}" height="{self.svg_height}" fill="white"/>
        <g transform="translate(0, {self.svg_height}) scale(1, -1)">
            {self.blackletter.svg_known(Point(1, 0), scale)}
        </g>
    </svg>
    """

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        open_action = QAction("Open", self)
        save_action = QAction("Save", self)

        update_birdfont_action = QAction("Update Birdfont", self)
        update_birdfont_action.triggered.connect(self.update_birdfont)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        # Add actions to the File menu
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(update_birdfont_action)

        file_menu.addSeparator()
        file_menu.addAction(exit_action)


    def update_birdfont(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Birdfont files (*.birdfont)"
        )

        if filename:
            br = BirdfontReader("cour.birdfont")
            br.load()

            br.replace_paths_by_unicode("a", self.blackletter.birdfont_path('a', 20))
            br.replace_paths_by_unicode("b", self.blackletter.birdfont_path('b', 20))
            br.replace_paths_by_unicode("c", self.blackletter.birdfont_path('c', 20))
            br.save()

