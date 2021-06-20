from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QDate
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QColor

from SpiderPlot import SpiderPlot
from common import yoyo_lookup, getTestKey

class ResultTableWidget(QWidget):
    def __init__(self, plot_lookup, parent = None, show_weight=False):
        super(QWidget, self).__init__(parent)

        # layout
        main_layout = QVBoxLayout()

        # plotting
        results_box = QGroupBox("Testresultate")
        results_box_layout = QVBoxLayout()
        self.results_box_table = QTableWidget()
        results_box_layout.addWidget(self.results_box_table)
        results_box.setLayout(results_box_layout)
        main_layout.addWidget(results_box)

        self.setLayout(main_layout)

        # configure results table
        self.show_weight = show_weight
        if self.show_weight:
            labels = ["Namen", "Test", "Gewicht [kg]", "Grösse [cm]", "Alter",
                      "5 m Sprint [s]", " ",
                      "20 m Sprint [s]", " ",
                      "Agility [s]", " ",
                      "Sprung [cm]", " ",
                      "Beweglichkeit [cm]", " ",
                      "Rumpfkraft [s]", " ",
                      "Yoyo Stufe", " "]
        else:
            labels = ["Namen", "Test", "Grösse [cm]", "Alter",
                      "5 m Sprint [s]", " ",
                      "20 m Sprint [s]", " ",
                      "Agility [s]", " ",
                      "Sprung [cm]", " ",
                      "Beweglichkeit [cm]", " ",
                      "Rumpfkraft [s]", " ",
                      "Yoyo Stufe", " "]
            

        self.plot_lookup = plot_lookup
        self.plot_percentiles = None

        self.results_box_table.setRowCount(0)
        self.results_box_table.setColumnCount(len(labels))
        self.results_box_table.setHorizontalHeaderLabels(labels)
        self.results_box_table.verticalHeader().setVisible(False)
        self.results_box_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.results_box_table.horizontalHeader()
        header.setMinimumSectionSize(30)
        for i in range(len(labels)):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

    def removeRow(self, test_key):
        for row in range(self.results_box_table.rowCount()):
            row_test_id = getTestKey(self.results_box_table.item(row, 0).text(),
                                     self.results_box_table.item(row, 1).text())

            if row_test_id == test_key:
                self.results_box_table.removeRow(row)
                return

    def removeRowsByName(self, name):
        rows_to_delete = []
        for row in range(self.results_box_table.rowCount()):
            name_row = self.results_box_table.item(row, 0).text()

            if name_row == name:
                rows_to_delete.append(row)

        for row in reversed(rows_to_delete):
            self.results_box_table.removeRow(row)
            

    def clearTable(self):
        for row in reversed(range(self.results_box_table.rowCount())):
            self.results_box_table.removeRow(row)            

    def addTestToTable(self, name, test_id, test_results):
        key = getTestKey(name, test_id)

        test_results['yoyo_converted'] = ' '
        for key_yoyo in yoyo_lookup.keys():
            if yoyo_lookup[key_yoyo] == int(round(test_results['yoyo'])):
                test_results['yoyo_converted'] = key_yoyo

        def setItems(start_col, field, precision, add_grade=False, grade_field = None):
            item = QTableWidgetItem(precision.format(test_results[field]))
            item.setTextAlignment(int(Qt.AlignRight | Qt.AlignVCenter))
            self.results_box_table.setItem(rowPosition , start_col, item)

            if add_grade:
                if grade_field is None:
                    grade_field = field

                if self.plot_percentiles:
                    sign = 1
                    if self.plot_lookup[grade_field]['invert']:
                        sign = -1

                    grade = 1
                    if sign * test_results[grade_field] > sign * self.plot_percentiles[grade_field][0]:
                        grade += 1
                    if sign * test_results[grade_field] > sign * self.plot_percentiles[grade_field][1]:
                        grade += 1
                    if sign * test_results[grade_field] > sign * self.plot_percentiles[grade_field][2]:
                        grade += 1

                    item = QTableWidgetItem(str(grade))
                else:
                    item = QTableWidgetItem("-")

                item.setBackground(QColor(224, 195, 30))
                item.setTextAlignment(int(Qt.AlignRight | Qt.AlignVCenter))
                self.results_box_table.setItem(rowPosition , start_col + 1, item)

        # add results to the table
        rowPosition = self.results_box_table.rowCount()
        self.results_box_table.insertRow(rowPosition)
        self.results_box_table.setItem(rowPosition , 0, QTableWidgetItem(str(name)))
        self.results_box_table.setItem(rowPosition , 1, QTableWidgetItem(str(test_id)))
        offset = 0
        if self.show_weight:
            setItems(2, 'weight', '{:.1f}', False)
            offset = 1
        setItems(2+offset, 'height', '{:.0f}', False)
        item = QTableWidgetItem(str(test_results['age']))
        item.setTextAlignment(int(Qt.AlignRight | Qt.AlignVCenter))
        self.results_box_table.setItem(rowPosition , 3+offset, item)
        setItems(4+offset, 'sprint5', '{:.2f}', True)
        setItems(6+offset, 'sprint20', '{:.2f}', True)
        setItems(8+offset, 'agility', '{:.2f}', True)
        setItems(10+offset, 'jump', '{:.0f}', True)
        setItems(12+offset, 'flexibility', '{:.1f}', True)
        setItems(14+offset, 'core', '{:.0f}', True)
        setItems(16+offset, 'yoyo_converted', '{0}', True, 'yoyo')

        del test_results['yoyo_converted']

    def setPlotPercentiles(self, percentiles):
        self.plot_percentiles = percentiles
