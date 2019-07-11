# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render , redirect
from .models import Team
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import *


def register_team(request):
    if request.method == "POST":
        team_name = request.POST["team_name"]
        password = request.POST["password"]
        obj = Team()
        if Team.objects.filter(name=team_name).exists():
            return HttpResponse(" Team Already Registered")
        obj.name = team_name
        obj.password =password
        obj.save()
        request.session["team_name"]=team_name
        return HttpResponse("Success")


def login_team(request):
    if request.method == "POST":
        print "in web_login"
        team_name = request.POST.get("team_name")
        password = request.POST.get("password")
        if Team.objects.filter(name=team_name).exists():
            obj = Team.objects.get(name=team_name)
            if check_password(password,obj.password):
                print team_name, password
                request.session['team_name'] = obj.team_name
                return HttpResponse("Success")
            else:
                return HttpResponse("Incorrect Password")

@csrf_exempt
def tryApi(request):
    if request.method == "POST":
        name = request.POST.get("name")
        print name
        return HttpResponse("Hi your request is received!")
    else:
        return HttpResponse("Error")


def main(request):
    return render(request, 'scrum/index.html', {})

def saveRecording(request):
    print "saved recording to bluemix and the path in the table"


