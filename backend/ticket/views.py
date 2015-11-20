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

<<<<<<< Updated upstream
=======
def queryDB(**name="",**grade="",**no="",**schoolID="",**societyID="",**requirement=""):
    return TicketApplication.objects.filter(
    name__contains=name,
    grade__contains=grade,
    no__contains=no,
    schoolID__cotains=schoolID,
    societyID__contains=societyID,
    requirement__contains=requirement
    )
>>>>>>> Stashed changes


def queryDB(d)
    return TicketApplication.objects.fliter(d)

def insertApplication(request):
    # Argument passed by POST (containing sensitive info)
    # Return success state in plain text ("success"/"illegal"/"failure"/"error")
    try:
<<<<<<< Updated upstream
=======
        ID=fliterPost(request,"ID")
        if not(validateIDCode(ID) or "code" in request.session fliterCode(request)==fliterPost(request,"captcha")):
            raise IOError(__ILLEGAL)
        TicketApplication.objects.create(
        name=fliterPost(request,"name"),
        grade=int(fliterPost(request,"grade")),
        no=int(fliterPost(request,"class")),
        schoolID=fliterPost(request,"schoolID"),
        societyID=fliterPost(request,"ID"),
        requirement=int(fliterPost(request,"requirement")),
        )
>>>>>>> Stashed changes
    except IOError,e:
        return HttpResponse(e)
    return HttpResponse(__SUCCESS)

def queryApplication(request):
    try:
        data={
        "name":fliterPost(request,"name")
        "grade":int(fliterPost(request,"grade"))
        "no":int(fliterPost(request,"class"))
        "schoolID":fliterPost(request,"schoolID")
        "societyID":fliterPost(request,"ID")
        "requirement":int(fliterPost(request,"requirement"))
        }
    except:
        pass

