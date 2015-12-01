from django.http import HttpResponse
from django.utils.html import *
from datetime import datetime
from json import dumps
import re

__ERROR="error"
__ILLEGAL="illegal"
__FAILURE="failure"
__SUCCESS="success"

def objectToDict(obj):
    d=dict()
    for i in columns:
        d[i]=getattr(obj,i)
    return d

class MyError(Exception):
    pass

class GuestDataHandler:

    data=dict()

    def __init__(self,columns,request):
        self.columns=columns
        self.request=request

    def fliterPost(self,name):
        try:
            return self.request.POST[name]
        except:
            raise MyError(__ERROR)

    def fliterCode(self):
        try:
            code=self.request.session["code"]
            del(request.session["code"])
            return code
        except:
            raise MyError(__ERROR)

    def validateData(self):
        if "code" in self.request.session and fliterCode()==fliterPost("captcha")):
            raise MyError(__ILLEGAL)
        for i in columns:
            if not i in self.data or len(self.data[i])>columns[i]:
                raise MyError(__ILLEGAL)

    def fetchData(self):
        try:
            for i in columns:
                tmp=fliterPost(i)
                if tmp:
                    self.data[i]=tmp
        except:
            raise MyError(__ERROR)

    def getData(self):
        fetchData()
        validateData()
        return self.data



class AdminDataHandler(GuestDataHandler):

    def isAdmin(self):
        return logined(self.request) and antiCSRF(self.request)

    def antiCSRF(self):
        return "HTTP_REFERER" in self.request.META and re.compile("^http://%s/" % self.request.get_host()).match(self.request.META["HTTP_REFERER"])

    def logined(self):
        return "logined" in self.request.session and self.request.session["logined"]==True
    
    def getData(self):
        if not isAdmin():
            raise MyError(__FAILURE)
        fetchData()
        return self.data

class DatabaseHandler:

    def __init__(self,columns,db)
        self.db=db
        self.columns=columns
    
    def insert(
        
