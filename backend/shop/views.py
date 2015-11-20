# from django.shortcuts import render
from django.http import HttpResponse
from shop.models import ShopApplication, Organization

# Create your views here.

class InvalidInput(Exception):
    pass

def n2b(x):
    if x == "1":
        return True
    elif x == "0":
        return False
    else:
        raise InvalidInput

def insertApplication(request):
    # Argument passed by POST (containing sensitive info)
    # Return success state in plain text ("success"/"illegal"/"failure"/"error")
    try:
        if not ("captcha" in request.POST and "code" in request.session and request.POST["captcha"] == request.session["code"]):
            return HttpResponse("illegal")

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

        org = Organization(grade = int(ownerGrade), no = int(ownerClass))
        org.save()

        data = ShopApplication(owner = owner, ownerContact = ownerContact, shopName = shopName, ownerType = int(ownerType), ownerOrganization = org , electricity = n2b(electricity), food = n2b(food), nonFood = n2b(nonFood), privilegeKey = privilegeKey)

        data.save()

        return HttpResponse("success")

    except:
        return HttpResponse("error")
