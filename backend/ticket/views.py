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

columns=["name","grade","no","schoolID","societyID","requirement"]

class MyError(Exception):
    pass

def fliterPost(request,name):
    try:
        return request.POST[name]
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
    return True
    try:
        return request.session["logined"]==True
    except:
        raise MyError(__FAILURE)

def validateData(request,data):

    if not(validateIDCode(data["societyID"]) and "code" in request.session and fliterCode(request)==fliterPost(request,"captcha")):
        raise MyError(__ILLEGAL)

    for i in columns:
        if not i in data:
            raise MyError(__ILLEGAL)

    if len(data["name"])>4 or len(data["schoolID"])>6 or data["requirement"]<1 or int(data["grade"])<1 or int(data["grade"])>3:
        raise MyError(__ILLEGAL)

def objectToDict(obj):
    d=dict()
    for i in columns:
        d[i]=getattr(obj,i)
    return d

def fetchData(request):
    try:
        data=dict()
        for i in columns:
            tmp=fliterPost(request,i)
            if tmp:
                data[i]=tmp
        return data
    except SyntaxError,e:
        raise MyError(__ILLEGAL)

def insertApplication(request):
    try:
        data=fetchData(request)
        validateData(request,data)
    except MyError,e:
        return HttpResponse(e)
    try:
        TicketApplication.objects.create(**data)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def queryApplication(request):
    try:
        if not logined(request):
            raise MyError(__FAILURE)
        data=fetchData(request)
        result=(list)(TicketApplication.objects.filter(**data))
        for key,val in enumerate(result):
            result[key]=objectToDict(val)
            result[key]["applicationID"]=val.pk
    except MyError,e:
        return HttpResponse(dumps({"state":e,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def deleteApplication(request):
    try:
        if not logined(request):
            raise MyError(__FAILURE)
        applicationID=fliterPost(request,"applicationID")
        TicketApplication.objects.get(pk=applicationID).delete();
    except MyError,e:
        return HttpResponse(e);
    return HttpResponse(__SUCCESS)

def modifyApplication(request):
    try:
        if not logined():
            raise MyError(__FAILURE)
        #delete
        applicationID=fliterPost(request,"applicationID")
        TicketApplication.objects.get(pk=applicationID).delete();
        #creat
        data=fetchData(request)
        data["py"]=applicationID
        validateData(request,data)
        TicketApplication.objects.create(**data)
        return insertApplication(request)
    except MyError,e:
        return HttpResponse(e);
    return HttpResponse(__SUCCESS)

def indexApplication(request):
    try:
        if not logined(request):
            raise MyError(__FAILURE)
        fromIndex=fliterPost(request,"from")
        toIndex=fliterPost(request,"to")
        result=(list)(TicketApplication.objects.all()[fromIndex:toIndex])
        for key,val in enumerate(result):
            result[key]=objectToDict(val)
            result[key]["applicationID"]=val.pk
    except MyError,e:
        return HttpResponse(dumps({"state":e,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def queryApplicationNumber(request):
    try:
        if not logined(request):
            raise MyError(__FAILURE)
        return HttpResponse(TicketApplication.objects.count())
    except:
        return HttpResponse(-1)

