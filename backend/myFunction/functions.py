from django.http import HttpResponse
from django.utils.html import *
from datetime import datetime
import re

ERROR_CODE="error"
ILLEGAL_CODE="illegal"
FAILURE_CODE="failure"
SUCCESS_CODE="success"

class MyError(Exception):
    pass

class GuestDataHandler:

    data=dict()
    columns=dict()

    def __init__(self,columns,request):
        self.columns=columns
        self.request=request

    def filterPost(self,name):
        if name in self.request.POST:
            return self.request.POST[name]
        else:
            raise MyError(ERROR_CODE)

    def filterCode(self):
        if "code" in self.request.session:
            code=self.request.session["code"]
            del(self.request.session["code"])
            return code
        else:
            raise MyError(ERROR_CODE)

    def validateCode(self):
        if "code" in self.request.session and self.filterCode()==self.filterPost("captcha"):
            return True
        else:
            return False

    def validateLength(self):
        for i in self.columns:
            if (not i in self.data) or len(self.data[i])>self.columns[i]:
                return False
        return True

    def fetchData(self):
        for i in self.columns:
            tmp=self.filterPost(i)
            if tmp:
                self.data[i]=tmp
    def validateData(self):
        return self.validateLength() and self.validateCode()

    def getData(self):
        self.fetchData()
        if self.validateData():
            return self.data
        else:
            raise MyError(ILLEGAL_CODE)


class AdminDataHandler(GuestDataHandler):

    def isAdmin(self):
        return self.logined() and self.antiCSRF()

    def antiCSRF(self):
        return "HTTP_REFERER" in self.request.META and re.compile("^http://%s/" % self.request.get_host()).match(self.request.META["HTTP_REFERER"])

    def logined(self):
        return "logined" in self.request.session and self.request.session["logined"]==True

    def validateLength(self):
        for i in self.data:
            if i in self.columns and len(self.data[i])>self.columns[i]:
                return False
        return True

    def validateData(self):
        return self.validateLength()
    
    def getData(self):
        if not self.isAdmin():
            raise MyError(FAILURE_CODE)
        self.fetchData()
        if self.validateData():
            return self.data
        else:
            raise MyError(ILLEGAL_CODE)

class DatabaseHandler:

    def __init__(self,columns,db):
        self.__db=db
        self.columns=columns
    
    def insert(self,data):
        data["timestamp"]=datetime.now()
        self.__db.objects.create(**data)
    
    def query(self,data):
        return self.objectsToDict( list(self.__db.objects.filter(**data)) )

    def delete(self,pk):
        self.__db.objects.get(pk=pk).delete()
    
    def modify(self,data):
        self.delete(data["pk"])
        self.insert(data)
        
    def index(self,start,length):
        return self.objectsToDict( list(self.__db.objects.all()[start:length]) )

    def objectsToDict(self,data):
        for key,val in enumerate(data):
            data[key]=self.objectToDict(val)
        return data

    def objectToDict(self,obj):
        d=dict()
        for i in self.columns:
            d[i]=getattr(obj,i)
        return d

    def getNumRecord(self):
        return self.__db.objects.all().count()


