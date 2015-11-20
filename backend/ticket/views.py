#from django.shortcuts import render
from django.http import HttpResponse
from ticket.models import *
from django.utils.html import *

__ERROR="error"
__ILLEGAL="illegal"
__FAILURE="failure"
__SUCCESS="success"

def validateIDCode(ID):  
    l=list(ID)
    if len(l)!=18:
        return False
    for i,it in enumerate(l):
        if it=='x' or it=='X':
            l[i]=10
        else:
            l[i]=int(it)
    sum=0  
    for i,it in enumerate(l):  
        weight = 2**(17-i) % 11  
        sum = (sum + int(it)*weight) % 11  
    return sum==1  


def fliterPost(request,name):
    try:
        return escape(request.POST[name])
    except:
        raise IOError(__ERROR)

def fliterCode(request):
    try:
        return escape(request.session["code"])
    except:
        raise IOError(__ERROR)



def insertApplication(request):
    try:
        ID=fliterPost(request,"ID")
        #if not validateIDCode(ID) or fliterCode(request)!=fliterPost(request,"captcha"):
        #    raise IOError(__ILLEGAL)
        TicketApplication.objects.create(
        name=fliterPost(request,"name"),
        grade=int(fliterPost(request,"grade")),
        no=int(fliterPost(request,"class")),
        schoolID=fliterPost(request,"schoolID"),
        societyID=fliterPost(request,"ID"),
        requirement=int(fliterPost(request,"requirement")),
        )
    except IOError,e:
        return HttpResponse(e)
    return HttpResponse(__SUCCESS)

