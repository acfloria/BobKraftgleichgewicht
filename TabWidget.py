from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from KurvenplotWidget import KurvenplotWidget
from KurvenplotWidget2 import KurvenplotWidget2

class CustomTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.initUi()

        self.tab_widget = QTabWidget()

        self.tabs = [self.kurvenplot,
                     self.kurvenplot2]

        self.tab_names = ['Kräftedarstellung Kurvenlage',
                          'Kräftedarstellung Kurvenlage Bobausrichtung']

        for i, tab in enumerate(self.tabs):
            self.tab_widget.addTab(self.tabs[i], self.tab_names[i])

        # Add tabs to widget
        self.layout.addWidget(self.tab_widget)

    def initUi(self):
        self.kurvenplot = KurvenplotWidget(self)
        self.kurvenplot2 = KurvenplotWidget2(self)

    def draw(self):
        self.kurvenplot.draw()
        self.kurvenplot2.draw()
