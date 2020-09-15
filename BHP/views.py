from django.shortcuts import render
import json
import pickle
import numpy as np
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

__data_columns = None
__locations = None
__model = None


def home(request):
    return render(request, "home.html")


def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0], 2)


def load_json():
    print("Loading saved model.....start")
    global __data_columns
    global __locations
    global __model
    with open("BHP/model/columns.json", 'r') as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]
    with open("BHP/model/bangalore_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)
    print("Loading saved model....Finish")


def getLocation():
    return __locations


if __name__ == "__main__":
    load_json()
    print("getting Location")

@csrf_exempt
def predict(request):
    if request.method == "POST":
        total_sqft = float(request.POST.get('total_sqft'))
        location = request.POST.get('location')
        bhk = int(request.POST.get('bhk'))
        bath = int(request.POST.get('bath'))
        load_json()
        response = json.dumps({'estimated_price':get_estimated_price(location, total_sqft, bhk, bath)})
        print(response)
        return HttpResponse(response)
