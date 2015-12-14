from myFunction.functions import *
from django.http import HttpResponse
from advertisement.models import *
from django.utils.html import *
from datetime import datetime
from json import dumps
from random import sample
from random import choice
import re

__ERROR="error"
__ILLEGAL="illegal"
__FAILURE="failure"
__SUCCESS="success"

guestColumns={"ownerName":20,"ownerContact":1000,"ownerType":1,"shopName":1000,"adPic":10000000,"isJoined":1}
adminColumns={"ownerName":20,"ownerContact":1000,"ownerType":1,"shopName":1000,"adPic":10000000,"pk":100,"isJoined":1,"isValidated":1}

class AdGuestDataHandler(GuestDataHandler):
    pass

class AdAdminDataHandler(AdminDataHandler):
    pass

class AdRandDataHandler(GuestDataHandler):

    def validateData(self):
        return self.validateLength()

def insertApplication(request):
    try:
        data=AdGuestDataHandler(guestColumns,request).getData()
        DatabaseHandler(guestColumns,AdvertisementApplication).insert(data)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def queryApplication(request):
    try:
        data=AdAdminDataHandler(adminColumns,request).getData()
        result=DatabaseHandler(adminColumns,AdvertisementApplication).query(data)
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    except:
        return HttpResponse(dumps({"state":__ERROR,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def guestQueryApplication(request):
    data=AdRandDataHandler({"pk":10},request).getData()
    result=DatabaseHandler(guestColumns,AdvertisementApplication).query(data)
    try:
        pass
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    except:
        return HttpResponse(dumps({"state":__ERROR,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def deleteApplication(request):
    try:
        pk=AdAdminDataHandler({"pk":10},request).getData()["pk"]
        DatabaseHandler(adminColumns,AdvertisementApplication).delete(pk)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def modifyApplication(request):
    try:
        data=AdAdminDataHandler(adminColumns,request).getData()
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
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    except:
        return HttpResponse(dumps({"state":__ERROR,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def queryApplicationNumber(request):
    try:
        data=AdminDataHandler({},request).getData()
    except:
        return HttpResponse(-1)
    return HttpResponse(DatabaseHandler(adminColumns,AdvertisementApplication).getNumRecord())

def getRandomAdvertisement(request):
    try:
        num=int(AdRandDataHandler({"num":10},request).getData()["num"])
        allAd=DatabaseHandler({"pk":10},AdvertisementApplication).query({})
        result=list()
        if num>len(allAd):
            for i in range(num):
                result.append(choice(allAd))
        else:
            result=sample(allAd,num)
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

