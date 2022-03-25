import json
import requests
from uk_covid19 import Cov19API

england_only = [
    'areaType=nation',
    'areaName=England'
]
cases_and_deaths = {
    "date": "date",
    "name": "areaName",
    "code": "areaCode",
    "cases": {
        "daily": "newCasesByPublishDate",
        "cumulative": "cumCasesByPublishDate"
    },
    "deaths": {
        "daily": "newDeathsByDeathDate",
        "cumulative": "cumDeathsByDeathDate"
    }
}

api = Cov19API(filters=england_only, structure=cases_and_deaths)


def get_covid_data():    
    data = api.get_json()
    return data