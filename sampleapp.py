from PySide2 import QtCore
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys


def main():
    app = QApplication(sys.argv)

    # Window creation
    window = QWidget()
    window.setGeometry(0, 0, 1000, 700)
    window.setWindowTitle("Pollutant Forecaster")

    grid = QGridLayout()
    window.setLayout(grid)

    pollutant_label = QLabel('Enter Pollutant')
    pollutant_edit = QLineEdit()

    state_label = QLabel('Enter State')
    state_edit = QLineEdit()

    begin_date_label = QLabel('Enter Beginning Date (MM/DD/YYYY): ')
    begin_date_edit = QLineEdit()

    end_date_label = QLabel('Enter End Date (MM/DD/YYYY): ')
    end_date_edit = QLineEdit()

    grid.addWidget(pollutant_label, 0, 0)
    grid.addWidget(pollutant_edit, 0, 1)

    grid.addWidget(state_label, 1, 0)
    grid.addWidget(state_edit, 1, 1)

    grid.addWidget(begin_date_label, 2, 0)
    grid.addWidget(begin_date_edit, 2, 1)

    grid.addWidget(end_date_label, 3, 0)
    grid.addWidget(end_date_edit, 3, 1)

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
