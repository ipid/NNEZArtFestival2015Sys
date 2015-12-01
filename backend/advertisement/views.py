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
        data=GuestDataHandler(guestColumns,request).getData()
        DatabaseHandler(AdvertisementApplication).insert(data)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)


def queryApplication(request):
    try:
        data=AdminDataHandler(adminColumns,request).getData()
        result=DatabaseHandler(adminColumns,AdvertisementApplication).query(data)
    except MyError,e:
        return HttpResponse(dumps({"state":e,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def deleteApplication(request):
    try:
        AapplicationID=dminDataHandler({"applicationID"},request).getData()["applicationID"]
        DatabaseHandler(adminColumns,AdvertisementApplication).deleteApplication(applicationID)
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
        data=AdminDataHandler({"from":10,"len":10},request).getData()
        result=DatabaseHandler(adminColumns,AdvertisementApplication).index(data["from"],data["len"])
    except MyError,e:
        return HttpResponse(dumps({"state":e,"result":[]}))
    except:
        return HttpResponse(dumps({"state":__ERROR,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def queryApplicationNumber(request):
    try:
        data=AdminDataHandler({},request).getData()
    except:
        return HttpResponse(-1)
    return HttpResponse(DatabaseHandler(adminColumns,AdvertisementApplication).getNumRecord())

