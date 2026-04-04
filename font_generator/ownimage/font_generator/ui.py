from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QAction
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QCheckBox, QSlider, QLabel, QMainWindow, QWidget, QFileDialog, QComboBox, QPushButton
)

from .birdfont_reader import BirdfontReader
from .blackletter import Blackletter
from .font_parameters import FontParameters
from .nib_type import NibType
from .vector import Vector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load previous window geometry
        self.settings = QSettings("YourCompany", "YourAppName")
        geometry = self.settings.value("windowGeometry")

        if geometry is not None:
            self.restoreGeometry(geometry)

        self.create_menu()
        self.setWindowTitle("Font Generator")

        layout = QVBoxLayout()

        self.svg_width = 2000
        self.svg_height = 600
        self.svg_widget = QSvgWidget()
        self.svg_widget.setFixedSize(self.svg_width, self.svg_height)
        layout.addWidget(self.svg_widget)

        # --- Create three side-by-side panels ---
        panels = QHBoxLayout()

        # ---------------- PANEL 1: GENERAL ----------------
        panel_general = QVBoxLayout()

        btn = QPushButton("Restart App")
        btn.clicked.connect(self.restart_app)
        restart_row = QHBoxLayout()
        restart_row.addWidget(btn)
        restart_row.addStretch()
        panel_general.addLayout(restart_row)

        self.show_all_chars = QCheckBox()
        self.show_all_chars.setChecked(True)
        self.show_all_chars.stateChanged.connect(self.update_svg)

        show_all_chars_row = QHBoxLayout()
        show_all_chars_row.addWidget(QLabel("Show all characters:"))
        show_all_chars_row.addWidget(self.show_all_chars)
        show_all_chars_row.addStretch()
        panel_general.addLayout(show_all_chars_row)

        self.sample_text = QComboBox()
        self.sample_text.setEditable(True)
        self.sample_text.lineEdit().setPlaceholderText("Enter characters of interest")
        self.sample_text.currentTextChanged.connect(self.update_sample_text)
        chars_of_interest_row = QHBoxLayout()
        chars_of_interest_row.addWidget(QLabel("Characters of interest:"))
        chars_of_interest_row.addWidget(self.sample_text)
        chars_of_interest_row.addStretch()
        panel_general.addLayout(chars_of_interest_row)

        self.filled = QCheckBox()
        self.filled.setChecked(True)
        self.filled.stateChanged.connect(self.update_svg)

        filled_row = QHBoxLayout()
        filled_row.addWidget(QLabel("Filled:"))
        filled_row.addWidget(self.filled)
        filled_row.addStretch()
        panel_general.addLayout(filled_row)

        self.scale = self.create_slider(panel_general, 10, 400, 40, "Scale")
        self.bezier_samples = self.create_slider(panel_general, 3, 50, 20, "Bezier Samples")
        self.circle_samples = self.create_slider(panel_general, 3, 50, 20, "Circle Samples")

        general_widget = QWidget()
        general_widget.setLayout(panel_general)
        panels.addWidget(general_widget)

        # ---------------- PANEL 2: PEN ----------------
        panel_pen = QVBoxLayout()

        self.pen_width = self.create_slider(panel_pen, 0, 100, 50, "Pen Width")
        self.pen_thickness = self.create_slider(panel_pen, 0, 100, 10, "Pen Thickness")
        self.pen_angle = self.create_slider(panel_pen, 0, 180, 90, "Pen Angle")

        pen_type_row = QHBoxLayout()
        pen_type_row.addWidget(QLabel("Pen Type:"))
        self.pen_type_combo = QComboBox()
        self.pen_type_combo.addItems([n.value for n in NibType])
        self.pen_type_combo.currentTextChanged.connect(self.update_svg)
        pen_type_row.addWidget(self.pen_type_combo)
        pen_type_row.addStretch()
        panel_pen.addLayout(pen_type_row)

        pen_stroke_row = QHBoxLayout()
        pen_stroke_row.addWidget(QLabel("Pen Stroke:"))
        self.pen_stroke_combo = QComboBox()
        self.pen_stroke_combo.addItems(list(self._pen_stroke_options().keys()))
        self.pen_stroke_combo.currentTextChanged.connect(self.update_svg)
        pen_stroke_row.addWidget(self.pen_stroke_combo)
        pen_stroke_row.addStretch()
        panel_pen.addLayout(pen_stroke_row)

        pen_widget = QWidget()
        pen_widget.setLayout(panel_pen)
        panels.addWidget(pen_widget)

        # ---------------- PANEL 3: METRICS ----------------
        panel_metrics = QVBoxLayout()

        self.ascender = self.create_slider(panel_metrics, 100, 1000, 700, "Ascender")
        self.tbar = self.create_slider(panel_metrics, 100, 1000, 500, "T Bar")
        self.x_height = self.create_slider(panel_metrics, 100, 1000, 300, "X Height")
        self.descender = self.create_slider(panel_metrics, 100, 1000, 700, "Descender")
        self.padding = self.create_slider(panel_metrics, 0, 100, 50, "Padding")

        metrics_widget = QWidget()
        metrics_widget.setLayout(panel_metrics)
        panels.addWidget(metrics_widget)

        # Add the panels to the main layout
        layout.addLayout(panels)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.update_svg()

    def closeEvent(self, event):
        # Save window geometry on exit
        self.settings.setValue("windowGeometry", self.saveGeometry())
        super().closeEvent(event)

    def create_slider(self, layout, min, max, value, name):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min, max)
        slider.setValue(value)
        slider.valueChanged.connect(self.update_svg)

        scale_row = QHBoxLayout()
        scale_row.addWidget(QLabel(f"{name}:"))
        scale_row.addWidget(slider)

        layout.addLayout(scale_row)

        return slider

    def update_sample_text(self):
        if not self.show_all_chars.isChecked():
            self.update_svg()

    def update_svg(self):
        radius = float(self.scale.value())
        svg_data = self.make_svg(radius)
        self.svg_widget.load(bytearray(svg_data, encoding="utf-8"))

    def get_font_parameters(self):
        width = self._width()
        return FontParameters(
            nib_type=NibType.of(self.pen_type_combo.currentText()),
            pen_width=width,
            pen_thickness=self._thickness(),
            pen_angle=self.pen_angle.value() / 2,
            filled=self.filled.isChecked(),
            ascender=self.ascender.value() / 100,
            tbar=self.tbar.value() / 100,
            x_height=self.x_height.value() / 100,
            baseline=0,
            descender=-self.descender.value() / 100,
            padding=self.padding.value() * width / 100,
            pen_stroke=self._pen_stroke(),
            bezier_samples=self.bezier_samples.value(),
            circle_samples=self.circle_samples.value()
        )

    def restart_app(self):
        import sys, subprocess
        from pathlib import Path

        script = Path(sys.argv[0]).resolve()
        cwd = script.parent

        log = cwd / "restart_log.txt"

        with open(log, "w") as f:
            f.write("Launching:\n")
            f.write(f"{sys.executable} {script}\n\n")
            f.flush()

            subprocess.Popen(
                [sys.executable, str(script)],
                cwd=str(cwd),
                stdout=f,
                stderr=f
            )

        self.close()
        sys.exit(0)

        self.close()
        sys.exit(0)

    def _width(self) -> float:
        return self.pen_width.value() / 100

    def _thickness(self) -> float:
        width = self._width()
        return width * self.pen_thickness.value() / 200

    def _pen_stroke_options(self) -> dict[str, list[tuple[float, float]]]:
        width = self._width()
        return {
            "black": [(0, width)],
            "half_and_two_quarters": [
                (0, width / 2),
                ((5 / 8) * width, width / 8),
                ((7 / 8) * width, width / 8)
            ],
            "four_lines": [
                (0, width / 7),
                ((2 / 7) * width, width / 7),
                ((4 / 7) * width, width / 7),
                ((6 / 7) * width, width / 7)
            ]
        }

    def _pen_stroke(self) -> list[tuple[float, float]]:
        selected = self.pen_stroke_combo.currentText()
        return self._pen_stroke_options()[selected]

    def make_svg(self, scale: float) -> str:
        fp = self.get_font_parameters()
        print(f"scale = {scale}")
        print(f"fp={fp}")
        self.blackletter = Blackletter(fp)

        offset = 300

        return f"""
    <svg width="{self.svg_width}" height="{self.svg_height}" viewBox="0 0 {self.svg_width} {self.svg_height}" 
        xmlns="http://www.w3.org/2000/svg">
    
        <rect x="0" y="{-offset}" width="{self.svg_width}" height="{self.svg_height + offset}" fill="white"/>
        <g transform="translate(0, {self.svg_height - offset}) scale(1, -1)">
            <line x1="0" y1="{fp.ascender * scale}" x2="{self.svg_width}" y2="{fp.ascender * scale}" stroke="black" stroke-width="1" />
            <line x1="0" y1="{fp.tbar * scale}" x2="{self.svg_width}" y2="{fp.tbar * scale}" stroke="black" stroke-width="1" />
            <line x1="0" y1="{fp.x_height * scale}" x2="{self.svg_width}" y2="{fp.x_height * scale}" stroke="black" stroke-width="1" />
            <line x1="0" y1="{fp.baseline * scale}" x2="{self.svg_width}" y2="{fp.baseline * scale}" stroke="black" stroke-width="1" />
            <line x1="0" y1="{fp.descender * scale}" x2="{self.svg_width}" y2="{fp.descender * scale}" stroke="black" stroke-width="1" />
            {self.svg(Vector(1, 0), scale, True)}
        </g>
    </svg>
    """

    def svg(self, start: Vector, scale: float, char_lines: bool) -> str:
        if self.show_all_chars.isChecked():
            return self.blackletter.svg_known(start, scale, char_lines)
        else:
            chars = ''.join(c for c in self.sample_text.currentText() if c in self.blackletter.known_glyphs())
            return self.blackletter.svg(start, chars, scale, char_lines)

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
