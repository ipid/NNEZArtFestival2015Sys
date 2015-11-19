# from django.shortcuts import render
from django.http import HttpResponse
from ticket.models import TicketApplication
from django.utils.html import *

# Create your views here.

__ERROR="error"
__ILLEGAL="illegal"
__FAILURE="failure"
__SUCCESS="success"

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

def validateInput(data):
    # Validate the input, return True if is valid, otherwise False
    if len(data.name)>4 or len(data.schoolID)>4:
        raise IOError(__ILLEGAL)

def extractInput(request):
    # Extract inputs from request
    data=TicketApplication()
    data.name=fliterPost(request,"name")
    data.organization.grade=fliterPost(request,"grade")
    data.organization.no=fliterPost(request,"class")
    data.schoolID=fliterPost(request,"schoolID")
    data.societyID=fliterPost(request,"ID")
    data.requirement=fliterPost(request,"requirement")
    if fliterPost(request,"captcha")!=fliterCode(request):
        raise IOError(__FAILURE)
    return data

def insertApplication(request):
    # Argument passed by POST (containing sensitive info)
    # Return success state in plain text ("success"/"illegal"/"failure"/"error")
    try:
        data = extractInput(request)
        validateInput(data)
    except IOError,e:
        return HttpResponse(e)
    try:
        data.save()
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

