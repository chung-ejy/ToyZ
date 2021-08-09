from django.shortcuts import render
from django.http.response import JsonResponse
import pickle
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import requests
from pymongo import MongoClient
@csrf_exempt
def backendView(request):
    info = json.loads(request.body.decode("utf-8"))
    try:
        client = MongoClient("localhost",27017)
        db = client["amazon_toys"]
        table = db["model"]
        data = table.find(show_record_id=False)
        model =  pd.DataFrame(list(data))
        m = pickle.loads(model["model"].item())
        complete = info
        complete["prediction"] = int(m.predict(pd.DataFrame([info])))
    except Exception as e:
        complete = info
        complete["prediction"] = "not found"
        print(str(e))
    return JsonResponse(complete,safe=False)