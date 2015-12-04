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

    __data=dict()
    __columns=dict()

    def __init__(self,columns,request):
        self.__columns=columns
        self.__request=request

    def filterPost(self,name):
        if name in self.__request.POST:
            return self.__request.POST[name]
        else:
            raise MyError(ERROR_CODE)

    def filterCode(self):
        if "code" in self.__request.session:
            code=self.__request.session["code"]
            del(self.__request.session["code"])
            return code
        else:
            raise MyError(ERROR_CODE)

    def validateCode(self):
        if "code" in self.__request.session and self.filterCode()==self.filterPost("captcha"):
            return True
        else:
            return False

    def validateData(self):
        for i in self.__columns:
            if (not i in self.__data) or len(self.__data[i])>self.__columns[i]:
                return False
        return True

    def fetchData(self):
        for i in self.__columns:
            tmp=self.filterPost(i)
            if tmp:
                self.__data[i]=tmp

    def getData(self):
        self.fetchData()
        if self.validateData() and self.validateCode():
            return self.__data
        else:
            raise MyError(ILLEGAL_CODE)


class AdminDataHandler(GuestDataHandler):

    __data=dict()
    __columns=dict()

    def __init__(self,columns,request):
        self.__columns=columns
        self.__request=request

    def isAdmin(self):
        return self.logined() and self.antiCSRF()

    def antiCSRF(self):
        return "HTTP_REFERER" in self.__request.META and re.compile("^http://%s/" % self.__request.get_host()).match(self.__request.META["HTTP_REFERER"])

    def logined(self):
        return "logined" in self.__request.session and self.__request.session["logined"]==True

    def validateData(self):
        for i in self.__data:
            if not i in self.columns or not len(self.__data[i])>self.__columns[i]:
                return False
        return True
    
    def getData(self):
        if not self.isAdmin():
            raise MyError(FAILURE_CODE)
        self.fetchData()
        if self.validateData():
            return self.__data
        else:
            raise MyError(ILLEGAL_CODE)

class DatabaseHandler:

    def __init__(self,columns,db):
        self.__db=db
        self.__columns=columns
    
    def insert(self,data):
        data["timestamp"]=datetime.now()
        self.__db.objects.create(**data)
    
    def query(self,data):
        return self.pkToApplicationID( list(self.__db.objects.filter(**data)) )

    def delete(self,pk):
        self.__db.objects.get(pk=pk).delete()
    
    def modify(self,data):
        self.delete(data["pk"])
        self.insert(data)
        
    def index(self,start,length):
        return self.objectsToDict( list(self.__db.objects.objects.all()[start:length]) )

    def objectsToDict(self,data):
        for key,val in enumerate(data):
            data[key]=self.objectToDict(val)
        return data

    def objectToDict(self,obj):
        d=dict()
        for i in self.__columns:
            d[i]=getattr(obj,i)
        return d

    def getNumRecord(self):
        return db.objects.all().count()


