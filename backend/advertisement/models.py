from django.db import models
from django import forms

PIC_ROOT="/pic/"

class AdvertisementApplication(models.Model):
    OWNERTYPE_CHOICES=(
            (0,0),
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
            (6,6),
    )
    OWNERGRADE_CHOICES=(
            (1,1),
            (2,2),
            (3,3),
    )
    ownerName=models.CharField(max_length=20)
    ownerContact=models.CharField(max_length=1000)
    ownerType=models.PositiveIntegerField(choices=OWNERTYPE_CHOICES)
    shopName=models.CharField(max_length=1000)
    shopNo=models.CharField(max_length=20,default="0")
    adPic=models.ImageField(upload_to=PIC_ROOT)
    isJoined=models.BooleanField(default=True)
    isValidated=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)

class AdvertisementApplicationForm(forms.ModelForm):
    class Meta:
        model=AdvertisementApplication
        fields=("ownerName","ownerContact","ownerType","shopName","adPic","isJoined")

class AdvertisementAdminForm(forms.ModelForm):
    class Meta:
        model=AdvertisementApplication
        fields=("ownerName","ownerContact","ownerType","shopName","adPic","isJoined","shopName","shopNo")

    def __init__(self,*args,**kwargs):
        super(AdvertisementAdminForm,self).__init__(*args,**kwargs)
        for i in self.fields:
            self.fields[i].required=False

