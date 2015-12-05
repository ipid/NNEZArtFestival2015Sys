"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import render
import ticket.views
import shop.views
import config.views
import captcha.views
import siteAdmin.views
import advertisement.views

urlpatterns = [
    url(r'^test.html$', lambda r: render(r, "test.html")),
    url(r'^login.html$', lambda r: render(r, "login.html")),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^api/ticket/insertApplication$', ticket.views.insertApplication),
    url(r'^api/ticket/queryApplication$', ticket.views.queryApplication),
    url(r'^api/ticket/modifyApplication$', ticket.views.modifyApplication),
    url(r'^api/ticket/deleteApplication$', ticket.views.deleteApplication),
    url(r'^api/ticket/indexApplication$', ticket.views.indexApplication),
    url(r'^api/ticket/queryApplicationNumber$', ticket.views.queryApplicationNumber),

    url(r'^api/advertisement/insertApplication$', advertisement.views.insertApplication),
    url(r'^api/advertisement/queryApplication$', advertisement.views.queryApplication),
    url(r'^api/advertisement/modifyApplication$', advertisement.views.modifyApplication),
    url(r'^api/advertisement/deleteApplication$', advertisement.views.deleteApplication),
    url(r'^api/advertisement/indexApplication$', advertisement.views.indexApplication),
    url(r'^api/advertisement/queryApplicationNumber$', advertisement.views.queryApplicationNumber),
    url(r'^api/advertisement/get$', advertisement.views.getRandomAdvertisement),

    url(r'^api/config/ifShowRequirementTextbox$', config.views.ifShowRequirementTextbox),
    url(r'^api/config/getHomepageButtonType$', config.views.getHomepageButtonType),

    url(r'^api/shop/insertApplication$', shop.views.insertApplication),
    url(r'^api/shop/queryApplication$', shop.views.queryApplication),
    url(r'^api/shop/modifyApplication$', shop.views.modifyApplication),
    url(r'^api/shop/deleteApplication$', shop.views.deleteApplication),
    url(r'^api/shop/indexApplication$', shop.views.indexApplication),
    url(r'^api/shop/queryApplicationNumber$', shop.views.queryApplicationNumber),

    url(r'^api/captcha/get$', captcha.views.getCAPTCHA),
    url(r'^api/captcha/verify', captcha.views.verifyCAPTCHA),
    url(r'^api/admin/login$', siteAdmin.views.login),
    url(r'^api/admin/logout$', siteAdmin.views.logout),
    url(r'^api/admin/isAdmin$', siteAdmin.views.isAdmin),
]
