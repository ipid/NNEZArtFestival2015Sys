#from django.shortcuts import render
from django.http import HttpResponse
from ticket.models import *
from django.utils.html import *

# Create your views here.

__ERROR="error"
__ILLEGAL="illegal"
__FAILURE="failure"
__SUCCESS="success"

def validateIDCode(l):  
    return True
    if len(l)!=18:
        return False
    sum = 0  
    for ii,n in enumerate(l):  
        i = 18-ii
        weight = 2**(i-1) % 11  
        sum = (sum + int(n)*weight) % 11  
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

def extractInput(request):
    name=fliterPost(request,"name")
    grade=int(fliterPost(request,"grade"))
    no=int(fliterPost(request,"class"))
    schoolID=fliterPost(request,"schoolID")
    societyID=fliterPost(request,"ID")
    requirement=int(fliterPost(request,"requirement"))

    if len(name)>4 or len(schoolID)>4 or requirement<=0 or not validateIDCode(societyID):
        raise IOError(__ILLEGAL)

    organization=Organization(grade=grade,no=no)
    data=TicketApplication(name=name,organization=organization,schoolID=schoolID,societyID=societyID,requirement=requirement)
    try:
        organization.save()
        data.save()
    except:
        raise IOError(__ERROR)


def insertApplication(request):
    # Argument passed by POST (containing sensitive info)
    # Return success state in plain text ("success"/"illegal"/"failure"/"error")
    try:
        extractInput(request)
    except IOError,e:
        return HttpResponse(e)
    return HttpResponse(__SUCCESS)

