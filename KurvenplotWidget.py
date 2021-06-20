from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QDoubleValidator
import numpy as np

from Kurvenplot import Kurvenplot

class KurvenplotWidget(QWidget):
    def __init__(self, plot_lookup, parent = None):
        super(QWidget, self).__init__(parent)

        # widgets radar plot
        self.plotting_widget = Kurvenplot(self)

        self.velocity = 100
        self.angle = 60
        self.radius = 50
        self.autocompute_angle = False

        self.velocity_edit = QLineEdit(self)
        self.velocity_edit.setValidator(QDoubleValidator(0, 150, 1))
        self.velocity_edit.setText(str(self.velocity))
        self.angle_edit = QLineEdit(self)
        self.angle_edit.setValidator(QDoubleValidator(0, 120, 1))
        self.angle_edit.setText(str(self.angle))
        self.radius_edit = QLineEdit(self)
        self.radius_edit.setValidator(QDoubleValidator(10, 200, 1))
        self.radius_edit.setText(str(self.radius))

        self.autocompute_box = QCheckBox("Winkel berechnen")

        # layout
        main_layout = QVBoxLayout()

        plot_box = QGroupBox("Diagramm")
        plot_box_layout = QVBoxLayout()
        plot_box_layout.addWidget(self.plotting_widget)
        plot_box.setLayout(plot_box_layout)
        main_layout.addWidget(plot_box, stretch=10)

        group_box = QGroupBox("Kurvenparameter")
        group_box.setMaximumWidth(800)
        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Geschwindigkeit [km/h]:"), self.velocity_edit)
        form_layout.addRow(QLabel("Kurvenradius [m]:"), self.radius_edit)
        form_layout.addRow(QLabel("Winkel [deg]:"), self.angle_edit)
        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box, alignment=Qt.AlignCenter)

        main_layout.addWidget(self.autocompute_box, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

        self.updatePlots()

        self.velocity_edit.editingFinished.connect(self.updateVelocity)
        self.angle_edit.editingFinished.connect(self.updateAngle)
        self.radius_edit.editingFinished.connect(self.updateRadius)
        self.autocompute_box.stateChanged.connect(self.updateAutocomputeAngle)

    def updatePlots(self):
        self.plotting_widget.updatePlots(self.angle / 180 * np.pi, self.velocity / 3.6, self.radius)

    def updateVelocity(self):
        val = self.velocity_edit.text()
        if val:
            self.velocity = float(val)

            if self.autocompute_angle:
                self.computeAngle()

            self.updatePlots()

    def updateAngle(self):
        if not self.autocompute_angle:
            val = self.angle_edit.text()
            if val:
                self.angle = float(val)
                self.updatePlots()

    def updateRadius(self):
        val = self.radius_edit.text()
        if val:
            self.radius = float(val)

            if self.autocompute_angle:
                self.computeAngle()

            self.updatePlots()

    def computeAngle(self):
        a_centrifugal = (self.velocity / 3.6) * (self.velocity / 3.6) / self.radius;
        a_gravity = 9.81
        
        self.angle = np.arctan2(a_centrifugal, a_gravity) * 180 / np.pi
        self.angle_edit.setText(str(int(self.angle)))

    def updateAutocomputeAngle(self, val):
        self.autocompute_angle = val
        if self.autocompute_angle:
            self.angle_edit.setReadOnly(True)
            self.computeAngle()
            self.updatePlots()

        else:
            self.angle_edit.setReadOnly(False)

    def draw(self):
        self.plotting_widget.redraw()
