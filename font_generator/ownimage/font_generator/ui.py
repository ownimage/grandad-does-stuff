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

        layout = QVBoxLayout()

        self.svg_width = 2000
        self.svg_height = 600
        self.svg_widget = QSvgWidget()
        self.svg_widget.setFixedSize(self.svg_width, self.svg_height)
        layout.addWidget(self.svg_widget)

        self.filled = QCheckBox()
        self.filled.setChecked(True)
        self.filled.stateChanged.connect(self.update_svg)

        filled_row = QHBoxLayout()
        filled_row.addWidget(QLabel("Filled:"))
        filled_row.addWidget(self.filled)
        filled_row.addStretch()

        layout.addLayout(filled_row)

        self.x_height = QSlider(Qt.Horizontal)
        self.x_height.setRange(100, 1000)
        self.x_height.setValue(300)
        self.x_height.valueChanged.connect(self.update_svg)

        x_height_row = QHBoxLayout()
        x_height_row.addWidget(QLabel("X Height:"))
        x_height_row.addWidget(self.x_height)

        layout.addLayout(x_height_row)

        self.ascender = QSlider(Qt.Horizontal)
        self.ascender.setRange(100, 1000)
        self.ascender.setValue(700)
        self.ascender.valueChanged.connect(self.update_svg)

        ascender_row = QHBoxLayout()
        ascender_row.addWidget(QLabel("Ascender:"))
        ascender_row.addWidget(self.ascender)

        layout.addLayout(ascender_row)

        self.tbar = QSlider(Qt.Horizontal)
        self.tbar.setRange(100, 1000)
        self.tbar.setValue(500)
        self.tbar.valueChanged.connect(self.update_svg)

        tbar_row = QHBoxLayout()
        tbar_row.addWidget(QLabel("T Bar:"))
        tbar_row.addWidget(self.tbar)

        layout.addLayout(tbar_row)

        self.descender = QSlider(Qt.Horizontal)
        self.descender.setRange(0, 1000)
        self.descender.setValue(700)
        self.descender.valueChanged.connect(self.update_svg)

        descender_row = QHBoxLayout()
        descender_row.addWidget(QLabel("Descender:"))
        descender_row.addWidget(self.descender)

        layout.addLayout(descender_row)

        self.scale = QSlider(Qt.Horizontal)
        self.scale.setRange(10, 400)
        self.scale.setValue(40)
        self.scale.valueChanged.connect(self.update_svg)

        scale_row = QHBoxLayout()
        scale_row.addWidget(QLabel("Scale:"))
        scale_row.addWidget(self.scale)

        layout.addLayout(scale_row)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.update_svg()

    def update_svg(self):
        radius = float(self.scale.value())
        svg_data = self.make_svg(radius)
        self.svg_widget.load(bytearray(svg_data, encoding="utf-8"))

    def get_fontParameters(self):
        return FontParameters(0.5, self.filled.isChecked(), self.ascender.value() / 100, self.tbar.value() / 100, self.x_height.value() / 100, 0,
                              -self.descender.value() / 100)

    def make_svg(self, scale: float) -> str:
        self.blackletter = Blackletter(self.get_fontParameters())

        offset = 300

        return f"""
    <svg width="{self.svg_width}" height="{self.svg_height}" viewBox="0 0 {self.svg_width} {self.svg_height}" 
        xmlns="http://www.w3.org/2000/svg">
    
        <rect x="0" y="{-offset}" width="{self.svg_width}" height="{self.svg_height + offset}" fill="white"/>
        <g transform="translate(0, {self.svg_height - offset}) scale(1, -1)">
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

            for k in self.blackletter.glyph_keys():
                br.replace_paths_by_unicode(k, self.blackletter.birdfont_path(k, 20))
            br.save()
