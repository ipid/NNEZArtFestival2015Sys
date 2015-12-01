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

guestColumns={"owner":20,"ownerContact":1000,"ownerType":1,"shopName":1000,"adUrl":1000}
adminColumns={"owner":20,"ownerContact":1000,"ownerType":1,"shopName":1000,"adUrl":1000,"ApplicationID":100}


def insertApplication(request):
    try:
        gdh=GuestDataHandler(guestColumns,request)
        data=gdh.getData()
        dbh=DatabaseHandler(AdvertisementApplication)
        dbh.insert(data)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)


def queryApplication(request):
    try:
        adh=AdminDataHandler(adminColumns,request)
        data=adh.getData()
        dbh=DatabaseHandler(adminColumns,AdvertisementApplication)
        result=dbh.query(data)
    except MyError,e:
        return HttpResponse(dumps({"state":e,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def deleteApplication(request):
    try:
        adh=AdminDataHandler({"applicationID",request)
        applicationID=adh.getData()["applicationID"]
        dbh=DatabaseHandler(adminColumns,AdvertisementApplication)
        dbh.deleteApplication(applicationID)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def modifyApplication(request):
    try:
        data=AdminDataHandler(adminColumns,request).getData()
        DatabaseHandler(adminColumns,AdvertisementApplication).modify(data)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def indexApplication(request):
    try:
        data=AdminDataHandler(adminColumns,request).getData()
        DatabaseHandler(adminColumns,AdvertisementApplication).index(data["from"],data["len"])
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def queryApplicationNumber(request):
    try:
        pass
    except:
        return HttpResponse(-1)


