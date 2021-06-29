import datetime
from PySide2 import QtCore
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
import datetime
import matplotlib.pyplot as plt
from Time_Series_Models.prophet_model import prediction



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

        self.begin_date_label = QLabel('Enter Beginning Date (MM/DD/YYYY): ')
        self.begin_date_edit = QLineEdit('This feature is not available yet (any input here will be ignored)')

        self.end_date_label = QLabel('Enter Ending Date (MM/DD/YYYY): ')
        self.end_date_edit = QLineEdit('This feature is not available yet (any input here will be ignored)')

        self.error_text = QLabel()

        self.button_one = QPushButton("Get Results")

        self.grid.addWidget(self.pollutant_label, 0, 0)
        self.grid.addWidget(self.pollutant_edit, 0, 1)

        self.grid.addWidget(self.city_label, 1, 0)
        self.grid.addWidget(self.city_edit, 1, 1)

        self.grid.addWidget(self.begin_date_label, 2, 0)
        self.grid.addWidget(self.begin_date_edit, 2, 1)

        self.grid.addWidget(self.end_date_label, 3, 0)
        self.grid.addWidget(self.end_date_edit, 3, 1)

        self.error_text.setMaximumSize(1000, 50)
        self.grid.addWidget(self.error_text, 4, 1)

        self.button_one.clicked.connect(self.__submit_input)
        self.grid.addWidget(self.button_one, 5, 1)

        self.show()


    def __validate_date(self, date):
        # returns True if valid, false if not
        try:
            if date[2] != '/' or date[5] != '/':
                return False, None

            month = date[:2]
            day = date[3:5]
            year = date[6:]

            entered_datetime = datetime.datetime(int(year), int(month), int(day))

            current_date = datetime.date.today().strftime('%m/%d/%Y')
            current_month = current_date[:2]
            current_day = current_date[3:5]
            current_year = current_date[6:]
            current_datetime = datetime.datetime(int(current_year), int(current_month), int(current_day))

            if entered_datetime > current_datetime:
                return True, entered_datetime
            else:
                return False, None
            
        except:
            return False, None


    def __submit_input(self):
        self.error_text.setText('')

        pollutants = ['NO2', 'O3', 'SO2', 'CO']

        pl = self.pollutant_edit.text()

        if pl not in pollutants:
            self.error_text.setText('Error: pollutant must be NO2, O3, SO2, or CO')
            print('Error: pollutant must be NO2, O3, SO2, or CO')
            return

        city = self.city_edit.text()

        date_feature_available = False

        if date_feature_available:
            bd = self.begin_date_edit.text()
            bd_valid, bd_datetime = self.__validate_date(bd)

            ed = self.end_date_edit.text()
            ed_valid, ed_datetime = self.__validate_date(ed)

            if bd_valid and ed_valid:
                if bd_datetime > ed_datetime:
                    self.error_text.setText('Error: ending date is before beginning date')
                    print('Error: ending date is before beginning date')
                    return
                else:
                    print('Date formats are correct')
            else:
                self.error_text.setText('Error: Date format(s) is/are incorrect')
                print('Error: Date format(s) is/are incorrect')
                return
        
        try:
            prediction(pl, city)
        except:
            self.error_text.setText('Error: something went wrong in prediction')
            print('Error: something went wrong in prediction')



def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()