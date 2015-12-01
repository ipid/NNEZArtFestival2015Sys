from django.http import HttpResponse
from django.utils.html import *
from datetime import datetime
import re

__ERROR="error"
__ILLEGAL="illegal"
__FAILURE="failure"
__SUCCESS="success"

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
            raise MyError(__ERROR)

    def filterCode(self):
        if "code" in self.__request.POST:
            code=self.__request.session["code"]
            del(request.session["code"])
            return code
        else:
            raise MyError(__ERROR)

    def validateCode(self):
        if "code" in self.__request.session and self.filterCode()==self.filterPost("captcha"):
            return False
        else:
            return True

    def validateData(self):
        for i in self.__columns:
            if not i in self.__data or len(self.__data[i])>self.__columns[i]:
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
            raise MyError(__ILLEGAL)


class AdminDataHandler(GuestDataHandler):

    def isAdmin(self):
        return self.logined(self.__request) and self.antiCSRF(self.__request)

    def antiCSRF(self):
        return "HTTP_REFERER" in self.__request.META and re.compile("^http://%s/" % self.__request.get_host()).match(self.__request.META["HTTP_REFERER"])

    def logined(self):
        return "logined" in self.__request.session and self.__request.session["logined"]==True

    def validateData(self):
        for i in self.__columns:
            if not len(self.__data[i])>self.__columns[i]:
                return False
        return True
    
    def getData(self):
        if not isAdmin():
            raise MyError(__FAILURE)
        fetchData()
        if self.validateData():
            return self.__data
        else:
            raise MyErro(ILLEGAL)

class DatabaseHandler:

    def __init__(self,columns,db):
        self.__db=db
        self.__columns=columns
    
    def insert(self,data):
        data["timestamp"]=datatime.now()
        __db.objects.creat(**data)
    
    def query(self,data):
        return self.pkToApplicationID( list(self.__db.objects.filter(**data)) )

    def delete(self,pk):
        __db.objects.get(pk=pk).delete()
    
    def modify(self,data):
        data["pk"]=data["applicationID"]
        del(data["applicationID"])
        self.delete(data["pk"])
        self.insert(data)
    
    def index(self,start,length):
        return self.pkToApplicationID( list(self.__db.objects.objects.all()[start:length]) )

    def pkToApplicationID(self,data):
        for key,val in enumerate(data):
            data[key]=self.objectToDict(val)
            data[key]["applicationID"]=val.pk
        return data

    def objectToDict(self,obj):
        d=dict()
        for i in self,__columns:
            d[i]=getattr(obj,i)
        return d

    def getNumRecord(self):
        return db.objects.all().count()


