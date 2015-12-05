from myFunction.functions import *
from django.http import HttpResponse
from shop.models import *
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

guestColumns={"ownerName":4,"ownerGrade":1,"ownerClass":2,"ownerContact":64,"shopName":32,"ownerType":1,"electricity":1,"food":1,"nonFood":1,"privilegeKey":8}
adminColumns={"ownerName":4,"ownerGrade":1,"ownerClass":2,"ownerContact":64,"shopName":32,"ownerType":1,"electricity":1,"food":1,"nonFood":1,"privilegeKey":8,"pk":10}

class ShopGuestDataHandler(GuestDataHandler):
    pass

class ShopAdminDataHandler(AdminDataHandler):
    pass

def insertApplication(request):
    data=ShopGuestDataHandler(guestColumns,request).getData()
    DatabaseHandler(guestColumns,ShopApplication).insert(data)
    try:
        pass
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def queryApplication(request):
    try:
        data=ShopAdminDataHandler(adminColumns,request).getData()
        result=DatabaseHandler(adminColumns,ShopApplication).query(data)
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    except:
        return HttpResponse(dumps({"state":__ERROR,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def deleteApplication(request):
    try:
        pk=ShopAdminDataHandler({"pk":10},request).getData()["pk"]
        DatabaseHandler(adminColumns,ShopApplication).delete(pk)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def modifyApplication(request):
    try:
        data=ShopAdminDataHandler(adminColumns,request).getData()
        DatabaseHandler(adminColumns,ShopApplication).modify(data)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def indexApplication(request):
    try:
        data=ShopAdminDataHandler({"from":10,"len":10},request).getData()
        result=DatabaseHandler(adminColumns,ShopApplication).index(data["from"],data["len"])
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    except:
        return HttpResponse(dumps({"state":__ERROR,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def queryApplicationNumber(request):
    try:
        ShopAdminDataHandler({},request).getData()
    except:
        return HttpResponse(-1)
    return HttpResponse(DatabaseHandler(adminColumns,ShopApplication).getNumRecord())

