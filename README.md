# AIRPrediction
(Framework) AIR Quality Forecast Model leveraging Time Series Models to enable timely preventive measures to reduce harmful impact on U.S. citizens.

## Dataset to Train the Time Series Model AIRPrediction (Prototype)
Since GitHub has a strict file limit of 100MB, we cannot upload the dataset to GitHub.
You need to include this csv file manually in the working directory: 
https://www.kaggle.com/sogun3/uspollution
pollution_us_2000_2016.csv(382.37 MB)

## Package Name for PIP Installation
pip install AIRPrediction

## Commands to Deploy AIRPrediction Model Using Flask API
1. Open your command prompt.
2. (command) pip install AIRPrediction.
3. Download pollution_us_2000_2016.csv(382.37 MB): https://www.kaggle.com/sogun3/uspollution
4. Extract pollution_us_2000_2016.csv(382.37 MB) in the src folder (e.g. C:\Users\AIRPrediction\src)
5. (command) cd (path to src folder. e.g. C:\Users\AIRPrediction\src)
6. (command) python3 forecast-flask-app.py
7. In command prompt, it will start importing modules using full dataset in a production environment (a development server), the model will be imported into flask app that returns predictions in seconds.
8. The URL will appear: http://127.0.0.1:5000/ 
9. Paste the URL to a web browser. 
10. (For Prototype Purposes Enter exactly) Enter the Pollutant: CO Enter the State : Washington Enter the Date : 07/27/2021 (or other future date.)
11. (Wait about five minutes) Creating the model on every input, it's repeating a process on every request.
12. The results of AQI will appear on the web browser. 

## Command to Run Sample App
(Once inside folder of installed framework)
python3 sampleapp.py 

## Repository Link
https://github.com/Data-for-Good-by-UF/AIR
