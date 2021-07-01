#!/usr/bin/env python3

# Pip package installation metadata file
# Install using e.g.:
#
#    "python3 setup.py develop" or "python3 setup.py install"
#
from setuptools import setup

NAME = "AIR"
VERSION = "1.0"
DESCRIPTION = """A lightweight service and Flask REST API 
  to predict the air quality index for selected US cities."""
AUTHOR = "TBD"
URL = "TBD"
PACKAGES = ["air"]
PY_MODULES = [
    "air_forecasting_service.py",
]
SCRIPTS = [
    # front-end Web API application
    "forecast-flask-app.py",
    "sampleapp.py",
    "prediction_example.py",
    "prediction_models.py",
]
DATA_FILES = [
    "pollution_us_2000_2016.csv",
]
REQUIRES = ["statsmodels", "flask", "flask-restful", "numpy", "pandas"]

setup(
    name=NAME,
    description=DESCRIPTION,
    author=AUTHOR,
    url=URL,
    packages=PACKAGES,
    py_modules=PY_MODULES,
    scripts=SCRIPTS,
    data_files=DATA_FILES,
    version=VERSION,
    platforms=["python>=3.7"],
    requires=REQUIRES,
)