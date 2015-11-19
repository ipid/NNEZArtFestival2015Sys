# from django.shortcuts import render
from django.http import HttpResponse
from random import randint
from PIL import Image, ImageDraw, ImageFont

# Create your views here.

def getCAPTCHA(request):
    a, b = randint(0, 99), randint(0, 99)
    request.session["code"] = str(a*b)

    image = Image.new("RGB", (100,25), "black")
    myFont = ImageFont.truetype("captcha/strangeFont.ttf", 20)
    draw = ImageDraw.Draw(image)
    draw.text((5, 0), "%s x %s = ?" % (a, b), font = myFont)

    response = HttpResponse(content_type = "image/png")
    image.save(response, "PNG")
    return response

def verifyCAPTCHA(request):
    return HttpResponse("1" if request.session.has_key("code") and request.GET.get("code", "") == request.session["code"] else "0")
