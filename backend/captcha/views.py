# from django.shortcuts import render
from django.http import HttpResponse
from random import randint
from PIL import Image, ImageDraw, ImageFont

# Create your views here.
w=200
h=70

dx=w/3
dy=h/2
fontsize=40

def getCAPTCHA(request):
    a, b = randint(0, 20), randint(0, 20)
    request.session["code"] = str(a*b)

    #image = Image.new("RGB", (w,h), "white")
    image = Image.new("RGB", (w,h), (randint(200,255),randint(200,255),randint(200,255)))
    myFont = ImageFont.truetype("captcha/strangeFont.ttf", fontsize)
    draw = ImageDraw.Draw(image)
    
    draw.text((randint(0,dx/2), randint(0,h-fontsize)), str(a), font=myFont,fill=0)
    draw.text((dx+randint(0,dx/2), randint(0,h-fontsize)), "X", font=myFont, fill=0)
    draw.text((2*dx+randint(0,dx/2), randint(0,h-fontsize)), str(b), font=myFont, fill=0)
    #draw.text((50, 0), "%s x %s = ?" % (a, b), font = myFont)

    for i in range(8):
        x1 = randint(0, w / 2)
        y1 = randint(0, h / 2)
        x2 = randint(w/2, w)
        y2 = randint(h/2, h)
        draw.line(((x1, y1), (x2, y2)), fill="black", width=randint(1,3))

    for i in range(100):
        x = randint(0, w)
        y = randint(0, h)
        draw.point((x,y), fill="black")

    response = HttpResponse(content_type = "image/png")
    image.save(response, "PNG")
    return response

def verifyCAPTCHA(request):
    return HttpResponse("1" if "code" in request.session and request.GET.get("code", "") == request.session["code"] else "0")
