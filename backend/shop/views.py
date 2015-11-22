# from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict
from shop.models import ShopApplication
from datetime import datetime
from json import dumps

# Create your views here.

def n2b(x):
    if x == "1":
        return True
    elif x == "0":
        return False
    else:
        raise InvalidInput

class InvalidInput(Exception):
    pass

def insertApplication(request):
    # Argument passed by POST (containing sensitive info)
    # Return success state in plain text ("success"/"illegal"/"failure"/"error")

    try:
        if not ("captcha" in request.POST and "code" in request.session and request.POST["captcha"] == request.session["code"]):
            return HttpResponse("illegal")
        del(request.session["code"])

        # Extract inputs
        owner = request.POST.get("owner", "")
        ownerContact = request.POST.get("ownerContact", "")
        shopName = request.POST.get("shopName", "")
        ownerType = request.POST.get("ownerType", "")
        ownerGrade = request.POST.get("ownerGrade", "")
        ownerClass = request.POST.get("ownerClass", "")
        electricity = request.POST.get("electricity", "")
        food = request.POST.get("food", "")
        nonFood = request.POST.get("nonFood", "")
        privilegeKey = request.POST.get("privilegeKey", "")

        # Validate the input

        try:
            if not all(map(lambda c: u'\u4e00' <= c <= u'\u9fa5', owner)):
                raise InvalidInput()
            if len(owner) > 4: raise InvalidInput()
            if len(ownerContact) > 64: raise InvalidInput()
            if len(shopName) > 32: raise InvalidInput()
            try:
                if not 0 <= int(ownerType) <= 6: raise InvalidInput()
                if not 10 <= int(ownerGrade) <= 12: raise InvalidInput()
                if not 1 <= int(ownerClass) <= 23: raise InvalidInput()
                n2b(electricity)
                n2b(food)
                n2b(nonFood)
            except ValueError:
                raise InvalidInput
            except InvalidInput:
                raise InvalidInput
            if not len(privilegeKey) == 8: raise InvalidInput
        except InvalidInput:
            return HttpResponse("illegal")

        # Save into DB

        data = ShopApplication(owner = owner, ownerContact = ownerContact, shopName = shopName, ownerType = int(ownerType), ownerGrade = int(ownerGrade), ownerClass = int(ownerClass), electricity = n2b(electricity), food = n2b(food), nonFood = n2b(nonFood), privilegeKey = privilegeKey, timestamp = datetime.now())

        data.save()

        return HttpResponse("success")

    except:
        return HttpResponse("error")

def antiCSRF(request):
    return "HTTP_REFERER" in request.META and request.META["HTTP_REFERER"] == request.get_host()

def logined(request):
    return "logined" in request.session and request.session["logined"] == True

def validate(request):
    return antiCSRF(request) and logined(request)

def applicationToDict(d):
    d = model_to_dict(d)
    d["applicationID"] = d["id"]
    del(d["id"])
    d["electricity"] = n2b(d["electricity"])
    d["food"] = n2b(d["food"])
    d["nonFood"] = n2b(d["nonFood"])
    del(d["timestamp"])
    return d

def indexApplication(request):
    try:
        if not validate(request):
            return HttpResponse("failure")
        try:
            lb = int(request.POST["from"])
            ub = int(request.POST["to"])
        except KeyError:
            return HttpResponse(dumps({"state": "illegal", "result": []}))
        except ValueError:
            return HttpResponse(dumps({"state": "illegal", "result": []}))
        answer = ShopApplication.objects.filter(pk__gte = lb, pk__lte = ub)
        answer = list(answer)
        answer = map(applicationToDict, answer)
        return HttpResponse(dumps({"state": "success", "result": answer}))
    except:
        return HttpResponse(dumps({"state": "error", "result": []}))

def queryApplicationNumber(request):
    try:
        if validate(request):
            return HttpResponse(str(ShopApplication.objects.all().count()))
        else:
            return HttpResponse("failure")
    except:
        return HttpResponse("error")

def queryApplication(request):
    try:

        args = {}

        # Extract inputs

        owner = request.POST.get("owner", "")
        ownerContact = request.POST.get("ownerContact", "")
        shopName = request.POST.get("shopName", "")
        ownerType = request.POST.get("ownerType", "")
        ownerGrade = request.POST.get("ownerGrade", "")
        ownerClass = request.POST.get("ownerClass", "")
        electricity = request.POST.get("electricity", "")
        food = request.POST.get("food", "")
        nonFood = request.POST.get("nonFood", "")
        privilegeKey = request.POST.get("privilegeKey", "")

        def addArgs(field, t = str):
            if field in request.POST:
                args[field] = t(request.POST[field])

        # Validate the input

        try:
            if "applicationID" in request.POST:
                args["pk"] = request.POST["applicationID"]
            addArgs("owner")
            addArgs("ownerContact")
            addArgs("shopName")
            addArgs("ownerType", int)
            addArgs("ownerGrade", int)
            addArgs("ownerClass", int)
            addArgs("electricity", n2b)
            addArgs("food", n2b)
            addArgs("nonFood", n2b)
            addArgs("privilegeKey")
        except InvalidInput:
            raise InvalidInput
        except ValueError:
            raise InvalidInput

        answer = ShopApplication.objects.filter(**args)
        answer = list(answer)
        answer = map(applicationToDict, answer)

        return HttpResponse(dumps({"state": "success", "result": answer}))

    except:
        return HttpResponse(dumps({"state": "error","result": []}))

def deleteApplication(request):
    try:
        if validate(request):
            try:
                i = request.POST["applicationID"]
                i = int(i)
            except KeyError:
                return HttpResponse("illegal")
            except ValueError:
                return HttpResponse("illegal")

            ShopApplication.objects.get(pk = i).delete()
            return HttpResponse("success")
        else:
            return HttpResponse("illegal")
    except:
        return HttpResponse("error")

def modifyApplication(request):
    try:
        if not applicationID in request.POST:
            return HttpResponse("illegal")

        # Extract inputs
        applicationID = request.POST.get("applicationID", "")
        try:
            data = ShopApplication.objects.get(pk = applicationID)
        except:
            return HttpResponse("illegal")

        data.owner = request.POST.get("owner", "")
        data.ownerContact = request.POST.get("ownerContact", "")
        data.shopName = request.POST.get("shopName", "")
        data.ownerType = request.POST.get("ownerType", "")
        data.ownerGrade = request.POST.get("ownerGrade", "")
        data.ownerClass = request.POST.get("ownerClass", "")
        data.electricity = request.POST.get("electricity", "")
        data.food = request.POST.get("food", "")
        data.nonFood = request.POST.get("nonFood", "")
        data.privilegeKey = request.POST.get("privilegeKey", "")

        # Save into DB

        data.save()

        return HttpResponse("success")
    except:
        return HttpResponse("error")
