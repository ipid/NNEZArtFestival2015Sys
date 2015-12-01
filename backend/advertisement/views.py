from myFunction.functions import *
from django.http import HttpResponse
from advertisement.models import *
from django.utils.html import *
from datetime import datetime
from json import dumps
import re

__ERROR="error"
__ILLEGAL="illegal"
__FAILURE="failure"
__SUCCESS="success"

columns={"owner":20,"ownerContact":1000,"ownerType":1,"shopName":1000,"adUrl":1000}

def objectToDict(obj):
    d=dict()
    for i in columns:
        d[i]=getattr(obj,i)
    return d

def insertApplication(request):
    try:
        data=fetchData(request)
        validateData(request,data)
        data["timestamp"]=datetime.now()
    except MyError,e:
        return HttpResponse(e)
    try:
        TicketApplication.objects.create(**data)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def queryApplication(request):
    try:
        if not isAdmin(request):
            raise MyError(__FAILURE)
        data=fetchData(request)
        if "applicationID" in request.POST and request.POST["applicationID"]:
            data["pk"]=request.POST["applicationID"]
        result=(list)(TicketApplication.objects.filter(**data))
        for key,val in enumerate(result):
            result[key]=objectToDict(val)
            result[key]["applicationID"]=val.pk
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def deleteApplication(request):
    try:
        if not isAdmin(request):
            raise MyError(__FAILURE)
        applicationID=fliterPost(request,"applicationID")
        TicketApplication.objects.get(pk=applicationID).delete()
    except MyError,e:
        return HttpResponse(e)
    return HttpResponse(__SUCCESS)

def modifyApplication(request):
    try:
        if not isAdmin(request):
            raise MyError(__FAILURE)
        #delete
        applicationID=fliterPost(request,"applicationID")
        TicketApplication.objects.get(pk=applicationID).delete()
        #creat
        data=fetchData(request)
        data["pk"]=applicationID
        TicketApplication.objects.create(**data)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def indexApplication(request):
    try:
        if not isAdmin(request):
            raise MyError(__FAILURE)
        fromIndex=fliterPost(request,"from")
        toIndex=fliterPost(request,"to")
        result=(list)(TicketApplication.objects.all()[fromIndex:toIndex])
        for key,val in enumerate(result):
            result[key]=objectToDict(val)
            result[key]["applicationID"]=val.pk
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def queryApplicationNumber(request):
    try:
        if not isAdmin(request):
            raise MyError(__FAILURE)
        return HttpResponse(TicketApplication.objects.count())
    except:
        return HttpResponse(-1)


