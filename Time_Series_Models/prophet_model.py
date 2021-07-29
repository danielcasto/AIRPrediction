import pandas as pd
from prophet import Prophet
from datetime import datetime


def prophet_prediction(pollutant, state, county, city, date):
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

    date_format = "%Y-%m-%d"

    start_date_temp = new_df.iloc[len(new_df.index)-1]['date']
    start_date = str(start_date_temp)[:10]

    start_date = datetime.strptime(start_date, date_format)
    target_date = datetime.strptime(date, date_format)
    date_difference = target_date - start_date

    new_df = new_df.rename(columns={"date": "ds",
                                    pollutant_choice: "y"})

    # use ffill (forward fill) to handle missing value filling the missing value from the previous day
    new_df = new_df.ffill()

    # model training
    prophet_model = Prophet()
    prophet_model.fit(new_df)

    # the parameter 'periods' represents the number of days you want to predict after 2016-04-30
    future = prophet_model.make_future_dataframe(periods = date_difference.days)

    forecast = prophet_model.predict(future)

    #print(forecast)

    if pollutant == "SO2" or pollutant == "NO2":
        pollutant_unit = "parts per billion (ppb)"
    elif pollutant == "O3" or pollutant == "CO":
        pollutant_unit = "parts per million (ppm)"
        
    temp = forecast[forecast['ds'] == date]
    output = list(x for x in temp["yhat"])

    #print(output)

    return output[0], pollutant_unit

