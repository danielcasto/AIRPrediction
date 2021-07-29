import datetime
import sys
import os
import csv
from timeit import timeit
from Time_Series_Models.prophet_model import prophet_prediction
from Time_Series_Models.ARIMA_model import arima_prediction


def validate_input(pollutant, state, county, city, date):
    validate = True
    return_message = ""
    valid_pollutants = ['NO2', 'O3', 'SO2', 'CO']
    entered_datetime = ""
    if pollutant not in valid_pollutants:
        validate = False
        return_message = "Error: Invalid Pollutant."
    else:
        if len(date) == 10:
            if date[2] != '/' or date[5] != '/':
                validate = False
                return_message = "Error: Invalid Date Format."

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
                validate = True
                month_string = str(entered_datetime.month)
                day_string = str(entered_datetime.day)
                if len(month_string) == 1:
                    month_string = '0' + month_string
                if len(day_string) == 1:
                    day_string = '0' + day_string
                entered_datetime = str(entered_datetime.year) + '-' + month_string + '-' + day_string

                with open("data/predictable_areas.csv") as file:
                    location_validator = csv.reader(file)
                    location_validation = False
                    state_validation = False
                    county_validation = False
                    city_validation = False
                    for row in location_validator:
                        if row[0] == state:
                            state_validation = True
                            if row[1] == county and row[2] == city:
                                location_validation = True
                        if row[1] == county:
                            county_validation = True
                        if row[2] == city:
                            city_validation = True
                    if not location_validation:
                        validate = False
                        if state_validation and county_validation and city_validation:
                            return_message = "Error: State, county, and city found. However, the combination of those parameters was not found in the dataset."
                        else:
                            return_message = "Error: Following location parameters not found in the dataset:"
                            if not state_validation:
                                return_message += " State,"
                            if not county_validation:
                                return_message += " County,"
                            if not city_validation:
                                return_message += " City."
                            if return_message[len(return_message) - 1] == ",":
                                return_message = return_message[0:(len(return_message) - 1)]
                                return_message += "."
            else:
                validate = False
                return_message = "Error: Invalid Date. Entered date must occur after current date."
        else:
            validate = False
            return_message = "Error: Invalid Date Format."
    return validate, return_message, entered_datetime


def prophet(pollutant, state, county, city, date):
    return prophet_prediction(pollutant, state, county, city, date)


def arima(pollutant, state, county, city, date):
    return arima_prediction(pollutant, state, county, city, date)


def compare_models(pollutant, state, county, city, date):
    validate, return_message, date = validate_input(pollutant, state, county, city, date)
    if validate:
        test_list = ((prophet, pollutant, state, county, city, date), (arima, pollutant, state, county, city, date))
        output_list = []
        for entry in test_list:
            output_list.append(timeit(lambda: entry[0](*entry[1:]), number=5))
        return output_list
    else:
        return return_message
