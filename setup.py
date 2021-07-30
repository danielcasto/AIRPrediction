from setuptools import setup

setup(
    name = 'AIRPrediction',
    version = '0.0.5',
    scripts = ['sampleapp.py', 'AIRPrediction.py', 'Time_Series_Models/ARIMA_model.py', 'Time_Series_Models/prophet_model.py', 'data/generate_predictable_city.py'],
    url = 'https://github.com/danielcasto/AIRPrediction',
    license = 'MIT',
    install_requires = ['PySide2', 'pystan==2.19.1.1', 'prophet', 'statsmodels'],
    data_files = ['data/pollution_us_2000_2016.csv', 'data/predictable_areas.csv'],

    entry_points={
        'console_scripts': [
            'sampleapp = sampleapp:main'
        ]
    }
)
