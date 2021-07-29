import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from datetime import datetime


def arima_prediction(pollutant, state, county, city, date):
    pollutant_choice = pollutant + " AQI"

    # read the csv file into a dataframe
    df = pd.read_csv('data/pollution_us_2000_2016.csv')

    # delete unnecessary data columns
    df = df.drop(columns=['Unnamed: 0', 'NO2 Units', 'O3 Units', 'SO2 Units', 'CO Units'])

    # delete duplicate data tuples
    df.drop_duplicates(inplace=True)

    # convert Date local to python date and time
    df['date'] = pd.to_datetime(df['Date Local'])
    df = df.drop(columns=['Date Local'])

    # compute mean AQI for each citiy for each date
    mean_aqi = df.groupby(['State','County','City', 'date'])[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']].mean()

    # reset index mean_aqi
    mean_aqi = mean_aqi.reset_index()

    # create subset of dataset to include only city and column selected for analysis
    temp_df = mean_aqi[(mean_aqi.State == state) & (mean_aqi.County == county) & (mean_aqi.City == city)]
    new_df = temp_df.loc[temp_df['City'] == city, ['date', pollutant_choice]]



    # use ffill (forward fill) to handle missing value filling the missing value from the previous day
    new_df = new_df.ffill()
    
    new_df = new_df.set_index("date")

    arima_model = ARIMA(new_df[pollutant_choice], order=(0, 1, 0))
    model_fit = arima_model.fit()


    date_format = "%Y-%m-%d"

    new_df = new_df.reset_index()

    start_date_temp = new_df.iloc[len(new_df.index)-1]['date']
    
    start_date = str(start_date_temp)[:10]
    start_date = datetime.strptime(start_date, date_format)
    target_date = datetime.strptime(date, date_format)
    date_difference = target_date - start_date

    mean_forecast = model_fit.forecast(steps=date_difference.days)

    if pollutant == "SO2" or pollutant == "NO2":
        pollutant_unit = "parts per billion (ppb)"
    elif pollutant == "O3" or pollutant == "CO":
        pollutant_unit = "parts per million (ppm)"


    return mean_forecast[0][len(mean_forecast[0])-1], pollutant_unit


