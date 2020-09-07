from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import *
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
import string
from random import *
import csv
import os
import json


def signin(request):
    return render(request, 'login.html', {})

def loginpro(request):
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('searchzoom')
    else:
        user = User.objects.get(email=username)
        if user is not None:
            login(request, user)
            return redirect('searchzoom')
        else:
            return redirect('signin')

def forgot(request):
    return render(request, 'forgot.html', {})

def send_reset_code(request):
    email = request.POST['email']
    letters = string.ascii_letters
    digits = string.digits
    chars = letters + digits
    min_length = 6
    max_length = 6
    def good_code():
        global code
        code = "".join(choice(chars) for x in range(randint(min_length, max_length)))
        try:
            checkcode = reset_code.objects.get(code=code)
            return good_code()
        except:
            pass
    good_code()

    try:
        user = User.objects.get(email=email)
        insert = reset_code(user=user, code=code)
        insert.save()
        subject = 'Hesita Reset Code'
        message = 'Your PASSWORD RESET CODE is'+code
        from_email = settings.EMAIL_HOST_USER
        to_list = [email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return redirect('enter_reset_code')
    except:
        return redirect("forgot")

def enter_reset_code(request):
    return render(request, 'enter_reset_code.html', {})


def resetpass(request):
    code = request.POST['code']
    try:
        resetpassuser = reset_code.objects.get(code=code)
        return render(request, 'resetpass.html', {'code':code})
    except:
        return redirect('enter_reset_code')

def resetpasspro(request, code):
    password = request.POST['pass']
    reppass = request.POST['reppass']
    if password == reppass:
        try:
            resetpassuser = reset_code.objects.get(code=code)
            user = resetpassuser.user
            user.set_password(password)
            user.save()
            resetpassuser.delete()
            return redirect('signin')
        except:
            return redirect('resetpass')
    else:
        return redirect('resetpass')


def searchzoom(request):
    if request.user.is_authenticated:
        return render(request, 'searchzoom.html', {})
    else:
        return redirect('signin')

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

