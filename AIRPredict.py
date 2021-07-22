import datetime
import sys
from timeit import timeit
from Time_Series_Models.prophet_model import prophet_prediction
from Time_Series_Models.prophet_model import arima_prediction


def validate_date(date):
    # returns True if valid, false if not
    if len(date) == 10:
        if date[2] != '/' or date[5] != '/':
            return False, "Error: Invalid Date."

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
            return True, ""
        else:
            return False, "Error: Invalid Date. Entered date must occur after current date."
    else:
        return False, "Error: Invalid Date."


def validate_input(pollutant, date, filename):
    validate = True
    return_message = ""
    valid_pollutants = ['NO2', 'O3', 'SO2', 'CO']
    if os.path.isfile(filename):
        if pollutant not in valid_pollutants:
            validate = False
            return_message = "Error: Invalid Pollutants."
        else:
            validate, return_message = validate_date(date)
    else:
        validate = False
        return_message = "Error: File not found."
    return validate, return_message


def prophet(pollutant, city, date, filename):
    validate, return_message = validate_input(pollutant, date, filename)
    if validate:
        return prophet_prediction(pollutant, city, date)
    else:
        return return_message


def arima(pollutant, city, date, filename):
    validate, return_message = validate_input(pollutant, date, filename)
    if validate:
        return arima_prediction(pollutant, city, date)
    else:
        return return_message


def compare_models(pollutant, city, date, filename):
    test_list = ((prophet, pollutant, city, date, filename), (arima, pollutant, city, date, filename))
    output_list = []
    if validate_input(pollutant, date, filename)[0]:
        for entry in test_list:
            output_list.append(timeit(lambda: entry[0](*entry[1:]), number=5))
        return output_list
    else:
        return validate_input(pollutant, date, filename)[1]
