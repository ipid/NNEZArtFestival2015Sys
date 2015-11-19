from django.shortcuts import render
from models import ShopApplication

# Create your views here.

def validateInput(data):
    # Validate the input, return True if is valid, otherwise False
    pass

def extractInput(request):
    # Extract inputs from request
    pass

def insertApplication(request):
    # Argument passed by POST (containing sensitive info)
    # Return success state in plain text ("success"/"illegal"/"failure"/"error")
    data = extractInput(request)
    try:
        if not validateInput(data):
            return HttpResponse("illegal")
        pass
    except:
        return HttpResponse("error")
