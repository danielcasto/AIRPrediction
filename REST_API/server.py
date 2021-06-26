from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
import numpy as np
import pickle as p


app = Flask(__name__)
api = Api(app)


@app.route('/forecast', methods=['GET'])
def make_prediction():
    data = request.get_json()
    prediction = np.array2string(prophet_model.predict(data))
    return jsonify(prediction)


if __name__ == "__main__":
    prophet_model_file = 'Time Series Models/prediction_prophet.pickle'
    prophet_model = p.load(open(prophet_model_file, 'rb'))
    app.run(debug=True)

