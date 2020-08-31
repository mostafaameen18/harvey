from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
import csv
import os
import json


def redirector(request):
    return redirect('searchzoom')

def searchzoom(request):
    return render(request, 'searchzoom.html', {})

def operate_location(request):
    import pickle
    import xgboost as xgb
    import pandas as pd
    file_name = os.path.join(settings.STATIC_ROOT, "model/model.pkl")
    try:
        # Get search result
        fileName = str(request.GET['searchText'])
        moderateName = '_'.join(fileName.split())
        moderateName = moderateName.replace(',', '')
        csvFileName = str(moderateName) + ".csv"
        csvFilePath = os.path.join(settings.MEDIA_ROOT, csvFileName)

        # load
        xgb_model_loaded = pickle.load(open(file_name, "rb"))

        test = pd.read_csv(csvFilePath)
        test.set_index('Unnamed: 0', inplace=True)

        # test
        result = xgb_model_loaded.predict(xgb.DMatrix(test))

        return HttpResponse(result)
    except:
        return HttpResponse('err')



def handlerr(request, exception=False):
    return render(request, '404.html', {})
