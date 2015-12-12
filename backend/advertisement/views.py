from django.http import HttpResponse
from advertisement.models import *
from django.utils.html import *
from datetime import datetime
from random import sample
from random import choice
from json import dumps
from django.core.serializers.json import DjangoJSONEncoder

__ERROR="error"
__ILLEGAL="illegal"
__FAILURE="failure"
__SUCCESS="success"

RETURNED_COLUMNS=[
"pk",
"ownerName",
"ownerContact",
"ownerType",
"shopName",
"shopNo",
"adPic",
"isJoined",
"isValidated",
]

def validateCode(request):
    return "captcha" in request.POST and "code" in request.session and request.POST["captcha"]==request.session["code"]

def validateUser(request):
    return "logined" in request.session and request.session["logined"]==True

def delEmptyDictVal(data):
    for key,val in data.items():
        if val=="":
            del(data[key])
    return data

def insertApplication(request):
    form=AdvertisementApplicationForm(request.POST,request.FILES)
    if validateCode(request) and form.is_valid():
        form.save()
        return HttpResponse(__SUCCESS)
    else:
        return HttpResponse(__ILLEGAL)

def queryApplication(request):
    if validateUser(request):
        form=AdvertisementAdminForm(request.POST,request.FILES)
        if form.is_valid():
            data=form.cleaned_data
            delEmptyDictVal(data)
            print data
            result=list(AdvertisementApplication.objects.filter(**data).values_list(*RETURNED_COLUMNS))
            result=dumps(result,cls=DjangoJSONEncoder)
            return HttpResponse(dumps({"state":__SUCCESS,"result":result}))
        else:
            return HttpResponse(dumps({"state":__ILLEGAL,"result":[]}))
    else:
        return dumps({"state":__FAILURE,"result":[]})

def deleteApplication(request):
    if validateUser(request):
        pk=request.POST["pk"]
        AdvertisementApplication.objects.get(pk=pk).delete()
        return HttpResponse(__SUCCESS)
    else:
        return HttpResponse(__FAILURE)

def modifyApplication(request):
    try:
        data=AdAdminDataHandler(adminColumns,request).getData()
        DatabaseHandler(adminColumns,AdvertisementApplication).modify(data)
    except MyError,e:
        return HttpResponse(e)
    except:
        return HttpResponse(__ERROR)
    return HttpResponse(__SUCCESS)

def indexApplication(request):
    try:
        data=AdminDataHandler({"from":10,"len":10},request).getData()
        result=DatabaseHandler(adminColumns,AdvertisementApplication).index(data["from"],data["len"])
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    except:
        return HttpResponse(dumps({"state":__ERROR,"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

def queryApplicationNumber(request):
    try:
        data=AdminDataHandler({},request).getData()
    except:
        return HttpResponse(-1)
    return HttpResponse(DatabaseHandler(adminColumns,AdvertisementApplication).getNumRecord())

def getRandomAdvertisement(request):
    try:
        num=int(AdRandDataHandler({"num":10},request).getData()["num"])
        allAd=DatabaseHandler({"adUrl":1000},AdvertisementApplication).query({})
        result=list()
        if num>len(allAd):
            for i in range(num):
                result.append(choice(allAd))
        else:
            result=sample(allAd,num)
    except MyError,e:
        return HttpResponse(dumps({"state":str(e),"result":[]}))
    return HttpResponse(dumps({"state":__SUCCESS,"result":result}))

