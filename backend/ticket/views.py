#from django.shortcuts import render
from django.http import HttpResponse
from ticket.models import *
from django.utils.html import *
from datetime import datetime
from json import dumps

__ERROR="error"
__ILLEGAL="illegal"
__FAILURE="failure"
__SUCCESS="success"

class MyError(Exception):
    pass

def fliterPost(request,name):
    try:
        return escape(request.POST[name])
    except:
        raise MyError(__ERROR)

def fliterCode(request):
    try:
        return escape(request.session["code"])
    except:
        raise MyError(__ERROR)

def validateIDCode(ID):  
    l=list(ID)
    if len(l)!=18:
        return False
    for i,it in enumerate(l):
        if it=='x' or it=='X':
            l[i]=10
        else:
            l[i]=int(it)
    sum=0  
    for i,it in enumerate(l):  
        weight = 2**(17-i) % 11  
        sum = (sum + int(it)*weight) % 11  
    return sum==1  

def validateAdmin(request):
    pass

def logined(request):
    try:
        return request.session["logined"]==True
    except:
        raise MyError(__FAILURE)

def validateData(request,data):
    try:
        ID=fliterPost(request,"ID")
    except:
        raise MyError(__ERROR)

    if not(validateIDCode(ID) or "code" in request.session and fliterCode(request)==fliterPost(request,"captcha")):
        raise MyError(__ILLEGAL)

    for key,val in enumerate(data):
        if(val==""):
            raise MyError(__ILLEGAL)

    if len(name)>4 or len(schoolID)>6 or requirement<1 or (grade<1 and grade>3):
        raise MyError(__ILLEGAL)

def queryDB(name,grade,no,schoolID,societyID,requirement,applicationID):
#def queryDB(**name="",**grade="",**no,**schoolID,**societyID,**requirement,**applicationID):
    return TicketApplication.objects.filter(
    name__contains=name,
    grade__contains=grade,
    no__contains=no,
    schoolID__cotains=schoolID,
    societyID__contains=societyID,
    requirement__contains=requirement,
    pk__contains=applicationID,
    )

def fetchData(request):
    try:
        return {
        "name":fliterPost(request,"name"),
        "grade":int(fliterPost(request,"grade")),
        "no":int(fliterPost(request,"class")),
        "schoolID":fliterPost(request,"schoolID"),
        "societyID":fliterPost(request,"ID"),
        "requirement":int(fliterPost(request,"requirement")),
        "timestamp":datetime.now(),
        }
    except SyntaxError,e:
        raise MyError(__ILLEGAL+"fetch")

def insertApplication(request):
    try:
        data=fetchData(request)
        #validateData(request,data)
    except MyError,e:
        return HttpResponse(e)

    try:
        TicketApplication.objects.create(**data)
    except:
        return HttpResponse(__ERROR)

    return HttpResponse(__SUCCESS)

def queryApplication(request):
    try:
        if not logined():
            raise MyError(__FAILURE)
        data=fetchDataNoExcept(request)
        result=(list)(queryDB(**data))
        #converting objects in list to dict
        for key,val in enumerate(result):
            result[key]=dict(val)
            result[key]["applicationID"]=val.pk
    except MyError,e:
        return HttpResponse(dumps({"state":e,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def deleteApplication(request):
    try:
        applicationID=fliterPost(request,"applicationID")
    except MyError,e:
        return HttpResponse(e);


def modifyApplication(request):
    pass

