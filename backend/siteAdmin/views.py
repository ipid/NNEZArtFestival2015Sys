#from django.shortcuts import render
from siteAdmin.models import *
from django.http import HttpResponse
import md5

# Create your views here.

__ERROR="error"
__FAILURE="failure"
__SUCCESS="success"
__ILLEGAL="illegal"

__SALT="DID YOU KNOW THAT I'M A LONG LONG SLAT LOLOLOLOLOL" 

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

def validateData(request):
    if filterCode(request)!=filterPost(request,"captcha"):
        raise MyError(__ILLEGAL)
    #password=md5.md5(filterPost(request,"password")).hexdigest()
    password=filterPost(request,"password")
    #UsersInfo.objects.create(username="haha",password="12345")
    #raise MyError("YEAH")
    if not UsersInfo.objects.filter(password=password).count():
        raise MyError(__FAILURE+password)

def setLogined(request):
    request.session["logined"]=True

def login(request):
    try:
        validateData(request)
    except MyError,e:
        return HttpResponse(e)
    setLogined(request)
    return HttpResponse(__SUCCESS)
    
