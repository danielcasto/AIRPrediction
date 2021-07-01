from flask import Flask, jsonify, render_template, request
from flask_restful import Api, Resource, reqparse, abort
import air_forecasting_service1

app = Flask(__name__)
api = Api(app, )

#prefix='C:\Users\Yuko's PC\Desktop\AIR_ver11\AIR_ver11\src'
forecast_get_args = reqparse.RequestParser()

forecast_get_args.add_argument("pollutant", type=str, help="Need pollutant")

locations = {}
location = None
code = None
date = None

@app.route('/')
def weather_dashboard():
    # print(location, code)

    return render_template('home.html')



@app.route('/results', methods=['GET', 'POST'])
def render_results():
    location = request.form['State']
    code = request.form['zipCode']
    date = request.form['Date']
    abort_location_doesnt_exist(location)

    # Need machine learning portion for this section
    afs = air_forecasting_service1.ForecastService(code)
    predicted_forecast = afs.predict(location)
    predicted_forecast = float("{0:.4f}".format(predicted_forecast[0]))
    data = {'date': date, 'state': location, 'code': code, 'predict': predicted_forecast}
    return render_template("results.html", data=data)

def abort_location_doesnt_exist(location):
    if False and location not in locations:
        abort(404, message="Location is not valid!")


class Forecast(Resource):
    def get(self, location):
        abort_location_doesnt_exist(location)
        # Need machine learning portion for this section
        afs = air_forecasting_service1.ForecastService("CO")
        predicted_forecast = afs.predict(location)
        data = {"forecast": predicted_forecast}
        return jsonify(data)

    # May remove later if needed
    def post(self, location):
        args = forecast_get_args.parse_args()
        locations[location] = args
        return locations[location], 201


api.add_resource(Forecast, "/forecast/<string:location>")

if __name__ == "__main__":
    app.run(debug=True)
