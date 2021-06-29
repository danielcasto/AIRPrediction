import requests

BASE = "http://127.0.0.1:5000/forecast"


def forecast(state, county, city):
    data = [state, county, city]
    response = requests.post(BASE, data)
    return response.json()
