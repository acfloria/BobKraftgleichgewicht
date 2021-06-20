import string
import sys

import PyQt5.QtCore as QtCore
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from MainWindow import MainWindow

class BobKraftVisApp(QObject):
    dataset_loaded = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.app = QApplication(sys.argv)

        self.window = MainWindow()

        self.connectActions()
        self.connectSignals()

    def run(self):
        #self.window.showMaximized()
        self.window.show()
        sys.exit(self.app.exec_())

    def connectActions(self):
        pass
#         self.window.tab_widget.ui_open_widget.load_db_button.clicked.connect(self.loadDataset)
# 
#         self.window.tab_widget.mod_player_widget.add_button.clicked.connect(self.addPlayer)
#         self.window.tab_widget.mod_player_widget.remove_button.clicked.connect(self.removePlayer)
# 
#         self.window.tab_widget.mod_test_widget.add_button.clicked.connect(self.addTest)
#         self.window.tab_widget.mod_test_widget.rm_button.clicked.connect(self.removeTest)
#         self.window.tab_widget.mod_test_widget.name_box_rm.currentTextChanged.connect(self.setRemoveTestYears)
#         self.window.tab_widget.mod_test_widget.year_box_rm.currentTextChanged.connect(self.setRemoveTestMonths)
# 
#         self.window.tab_widget.edit_db_widget.name_box.currentTextChanged.connect(self.setEditDbYears)
#         self.window.tab_widget.edit_db_widget.year_box.currentTextChanged.connect(self.setEditDbMonths)
#         self.window.tab_widget.edit_db_widget.month_box.currentTextChanged.connect(self.setEditDbTestResult)
#         self.window.tab_widget.edit_db_widget.save_button.clicked.connect(self.updateDbResults)
# 
#         self.window.tab_widget.plot_widget.spider_widget.name_box.currentTextChanged.connect(self.setTestsListSpiderPlot)
#         self.window.tab_widget.plot_widget.spider_widget.add_button.clicked.connect(self.addTestToSpiderPlot)
#         self.window.tab_widget.plot_widget.progress_widet.add_button.clicked.connect(self.addTestToProgressPlot)


    def connectSignals(self):
        pass
#         self.dataset_loaded.connect(self.onDatasetLoaded)
#         self.players_changed.connect(self.onPlayersChanged)
#         self.tests_changed.connect(self.onTestsChanged)
#         self.dataset_changed.connect(self.onDatasetChanged)
