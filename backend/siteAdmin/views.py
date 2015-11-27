#from django.shortcuts import render
from siteAdmin.models import *
from django.http import HttpResponse
import md5

# Create your views here.

__ERROR="error"
__FAILURE="failure"
__SUCCESS="success"
__ILLEGAL="illegal"

class MyError(Exception):
    pass

def filterPost(request,name):
    try:
        return request.POST[name]
    except:
        raise MyError(__ERROR)

def filterCode(request):
    try:
        return request.session["code"]
    except:
        raise MyError(__ERROR)

def isLogined(request):
    if not "logined" in request.session:
        raise MyError(__ERROR)
    return request.session["logined"]

def setLogined(request):
    try:
        request.session["logined"]=True
    except:
        raise MyError(__ERROR)

def validateData(request):
    if filterCode(request)!=filterPost(request,"captcha"):
        raise MyError(__ILLEGAL)
    password=filterPost(request,"password")
    if not UsersInfo.objects.filter(password=password).count():
        raise MyError(__FAILURE+password)
    return True

def login(request):
    try:
        if validateData(request):
            setLogined(request)
    except MyError,e:
        return HttpResponse(e)
    return HttpResponse(__SUCCESS)

def logout(request):
    try:
        if not isLogined(request):
            del(request.session["logined"])
        else:
            raise MyError(__FAILURE)
    except MyError,e:
        return HttpResponse(e)
    return HttpResponse(__SUCCESS)

