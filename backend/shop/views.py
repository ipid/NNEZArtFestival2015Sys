from myFunction.functions import *
from django.http import HttpResponse
from shop.models import *
from django.utils.html import *
from datetime import datetime
from json import dumps
from random import sample,choice,random,randint
from md5 import md5
import re

guestColumns={"ownerName":4,"ownerGrade":1,"ownerClass":2,"ownerContact":64,"shopName":32,"ownerType":1,"electricity":1,"food":1,"nonFood":1,"privilegeKey":8}
adminColumns={"ownerName":4,"ownerGrade":1,"ownerClass":2,"ownerContact":64,"shopName":32,"ownerType":1,"electricity":1,"food":1,"nonFood":1,"privilegeKey":8,"pk":10}


def PrivilegeKeyGenerator():
    num=raw_input("Enter the number of keys you want to generate: ")
    print "Generating Keys..."
    for i in range(int(num)):
        fromIndex=randint(0,24)
        key=md5(str(random())).hexdigest()[fromIndex:fromIndex+8]
        PrivilegeKey.objects.get_or_create(privilegeKey=key)
        print key
    print "Finished!"


class ValidateDataTypeMixin:
    def validateDataType(self):
        try:
            ownerClass=int(self.data["ownerClass"])
            ownerGrade=int(self.data["ownerGrade"])
            ownerType=int(self.data["ownerType"])
            electricity=int(self.data["electricity"])
            food=int(self.data["food"])
            nonFood=int(self.data["nonFood"])
            privilegeKey=self.data["privilegeKey"]
        except:
            return False
        if not ( len(privilegeKey)==8 and ownerGrade>=1 and ownerGrade<=3 and ownerType>=0 and ownerType<=6 and (food==1 or food ==0) and (nonFood==1 or nonFood==0) and (electricity==1 or electricity==0) ):
            return False
        return True

class ValidatePrivilegeKeyMixin:
    def validatePrivilegeKey(self):
        privilegeKey=self.data["privilegeKey"]
        if privilegeKey=="00000000":
            return True
        else:
            result=DatabaseHandler(["privilegeKey"],PrivilegeKey).query({"privilegeKey":privilegeKey})
            return len(result)==1

class ShopGuestDataHandler(GuestDataHandler,ValidatePrivilegeKeyMixin,ValidateDataTypeMixin):
    def validateData(self):
        return self.validateCode() and self.validateLength() and self.validateDataType() and self.validatePrivilegeKey()

class ShopAdminDataHandler(AdminDataHandler):
    pass

def insertApplication(request):
    try:
        data=ShopGuestDataHandler(guestColumns,request).getData()
        dh=DatabaseHandler(adminColumns,ShopApplication)
        result=dh.query({"privilegeKey":data["privilegeKey"]})
        if len(result)==1 and data["privilegeKey"]!="00000000":
            data["pk"]=result[0]["pk"]
            dh.modify(data)
        else:
            DatabaseHandler(guestColumns,ShopApplication).insert(data)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(ERROR_CODE)
    return HttpResponse(SUCCESS_CODE)

def queryApplication(request):
    try:
        data=ShopAdminDataHandler(adminColumns,request).getData()
        result=DatabaseHandler(adminColumns,ShopApplication).query(data)
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    except:
        return HttpResponse(dumps({"state":ERROR_CODE,"result":[]}))
    return HttpResponse(dumps({"state":SUCCESS_CODE,"result":result}))

def deleteApplication(request):
    try:
        pk=ShopAdminDataHandler({"pk":10},request).getData()["pk"]
        DatabaseHandler(adminColumns,ShopApplication).delete(pk)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(ERROR_CODE)
    return HttpResponse(SUCCESS_CODE)

def modifyApplication(request):
    try:
        data=ShopAdminDataHandler(adminColumns,request).getData()
        DatabaseHandler(adminColumns,ShopApplication).modify(data)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(ERROR_CODE)
    return HttpResponse(SUCCESS_CODE)

def indexApplication(request):
    try:
        data=ShopAdminDataHandler({"from":10,"len":10},request).getData()
        result=DatabaseHandler(adminColumns,ShopApplication).index(data["from"],data["len"])
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    except:
        return HttpResponse(dumps({"state":ERROR_CODE,"result":[]}))
    return HttpResponse(dumps({"state":SUCCESS_CODE,"result":result}))

def queryApplicationNumber(request):
    try:
        ShopAdminDataHandler({},request).getData()
    except:
        return HttpResponse(-1)
    return HttpResponse(DatabaseHandler(adminColumns,ShopApplication).getNumRecord())

def dumpApplication(request):
    pass
