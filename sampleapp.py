from PySide2 import QtCore
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
import datetime
import time
from AIRPrediction import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1000, 700)
        self.setWindowTitle("Pollutant Forecaster")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.pollutant_label = QLabel('Enter Pollutant (NO2, O3, SO2, or CO):')
        self.pollutant_edit = QLineEdit()

        self.city_label = QLabel('Enter City: ')
        self.city_edit = QLineEdit()

        self.county_label = QLabel('Enter County: ')
        self.county_edit = QLineEdit()

        self.state_label = QLabel('Enter State: ')
        self.state_edit = QLineEdit()

        self.end_date_label = QLabel('Enter Future Date (MM/DD/YYYY): ')
        self.end_date_edit = QLineEdit()

        selector = QLabel('Select a forecasting method')
        self.radiobtn1 = QRadioButton('Prophet Model')
        self.radiobtn1.setMinimumHeight(40)
        self.radiobtn2 = QRadioButton('Arima')
        self.radiobtn2.setMinimumHeight(40)
        self.radiobtn3 = QRadioButton('Compare Both Models')
        self.radiobtn3.setMinimumHeight(40)

        self.msg_text = QLabel()

        self.button_one = QPushButton("Get Results")

        self.grid.addWidget(self.pollutant_label, 0, 0)
        self.grid.addWidget(self.pollutant_edit, 0, 1)

        self.grid.addWidget(self.state_label, 1, 0)
        self.grid.addWidget(self.state_edit, 1, 1)

        self.grid.addWidget(self.county_label, 2, 0)
        self.grid.addWidget(self.county_edit, 2, 1)

        self.grid.addWidget(self.city_label, 3, 0)
        self.grid.addWidget(self.city_edit, 3, 1)

        self.grid.addWidget(self.end_date_label, 4, 0)
        self.grid.addWidget(self.end_date_edit, 4, 1)

        self.grid.addWidget(selector, 5, 0)
        self.grid.addWidget(self.radiobtn1, 6, 0)
        self.grid.addWidget(self.radiobtn2, 6, 1)
        self.grid.addWidget(self.radiobtn3, 6, 2)

        self.msg_text.setMaximumSize(1000, 50)
        self.grid.addWidget(self.msg_text, 5, 1)

        self.button_one.clicked.connect(self.__submit_input)
        self.grid.addWidget(self.button_one, 7, 1)

        self.show()

    def __submit_input(self):
        self.msg_text.setText('')
        pl = self.pollutant_edit.text()
        state = self.state_edit.text()
        county = self.county_edit.text()
        city = self.city_edit.text()
        date_feature_available = True
        if date_feature_available:
            ed = self.end_date_edit.text()
        try:
            self.msg_text.setText('Validating Input...')
            validate, return_message, date_string = validate_input(pl, state, county, city, ed)
            if self.radiobtn1.isChecked():
                if validate:
                    self.msg_text.setText('Running Prophet Model...')
                    prophet_result, pollutant_unit = prophet_prediction(pl, state, county, city, date_string)
                    self.msg_text.setText(f'The forecast for {pl} in {city}, {county}, {state} is {prophet_result} {pollutant_unit}')
                else:
                    self.msg_text.setText(return_message)
            elif self.radiobtn2.isChecked():
                if validate:
                    self.msg_text.setText('Running ARIMA Model...')
                    arima_result, pollutant_unit = arima_prediction(pl, state, county, city, date_string)
                    self.msg_text.setText(f'The forecast for {pl} in {city}, {county}, {state} is {arima_result} {pollutant_unit}')
                else:
                    self.msg_text.setText(return_message)
            elif self.radiobtn3.isChecked():
                start_one = time.time()
                prophet_result, pollutant_unit = prophet_prediction(pl, state, county, city, date_string)
                end_one = time.time()
                prophet_time = end_one - start_one
                start_two = time.time()
                arima_result, pollutant_unit = arima_prediction(pl, state, county, city, date_string)
                end_two = time.time()
                arima_time = end_two - start_two
                self.msg_text.setText(f'The prophet forecast for {pl} in {city}, {county}, {state} is {prophet_result} {pollutant_unit} and took'
                                        f'\n{prophet_time} seconds.'
                                        f'\nThe ARIMA forecast for {pl} in {city}, {county}, {state} is {arima_result} {pollutant_unit} and took'
                                        f'\n{arima_time} seconds.')

        except:
            self.msg_text.setText('Error: something went wrong in prediction')
            print('Error: something went wrong in prediction')


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
