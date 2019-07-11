# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


import os.path
from django.shortcuts import render , redirect
from .models import Team
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import tempfile
from django.core.files import File
import logging
import smtplib


from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import json

import  json
import base64

logger = logging.getLogger(__name__)
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


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
def getRecording(request):
    # if request.method == "POST":
    #     name = request.POST.get("name")
    #     print name
    #     return HttpResponse("Hi your request is received!")
    # else:
    data = json.loads(request.body)
    file_name=data["file_name"]
    file_data=data["file_data"]
    audiofile_byte = base64.b64decode(file_data)
    logger.debug(audiofile_byte)
    logger.debug(file_name)
    path = '~/'
    # file = ContentFile(audiofile_byte)
    path=SITE_ROOT+'/static/recording.wav'
    with open(path, 'w+') as output:
        output.write(audiofile_byte)

    # with tempfile.TemporaryFile(mode='w') as f:
    #     audiofile_byte.write_to_fp(f)
    #     file_name = '{}.wav'.format(file_name)
    #     audiofile_byte.save(file_name, File(file=f))

    # file_name = default_storage.save(file_name, file)

    return HttpResponse("HIIII Pooja!!!!")


def writeToFile(data):
    path2=SITE_ROOT+'/static/recording.txt'
    with open(path2, "w+") as transcript:
        transcript.write(json.dumps(data, indent=2))


def sendEmail():
    MY_ADDRESS = "ibmhackathon@gmail.com"
    PASSWORD = "sasasadadad"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # s.starttls()
    # s.login(MY_ADDRESS, PASSWORD)


def speechToText():
    path=SITE_ROOT+'/static/recording.wav'
    speech_to_text = SpeechToTextV1(
        iam_apikey='9e0ri-mtT_R8DicTjLTNkRe9T1WJFxHdkFBYobAmlxp2',
        url='https://gateway-wdc.watsonplatform.net/speech-to-text/api/v1/recognize'
    )

    speech_to_text.disable_SSL_verification()
    jsonresult = ""
    class MyRecognizeCallback(RecognizeCallback):
        def __init__(self):
            RecognizeCallback.__init__(self)

        def on_data(self, data):
            jsonData = json.dumps(data)
            print(jsonData)
            writeToFile(jsonData)
            # sendEmail()

        def on_error(self, error):
            print('Error received: {}'.format(error))

        def on_inactivity_timeout(self, error):
            print('Inactivity timeout: {}'.format(error))

    myRecognizeCallback = MyRecognizeCallback()

    with open(path, 'rb') as audio_file:
        audio_source = AudioSource(audio_file)
        speech_to_text.recognize_using_websocket(
            audio=audio_source,
            content_type='audio/mp3',
            recognize_callback=myRecognizeCallback,
            model='en-US_BroadbandModel',
            interim_results=True,
            speaker_labels=True)


@csrf_exempt
def playRecording(request):
    speechToText()
    print "called ibm watson"
    return render(request,'scrum/recording.html',{"recording":"/static/recording.wav","name":"recording.wav"})

def main(request):
    return render(request, 'scrum/index.html', {})

def saveRecording(request):
    print "saved recording to bluemix and the path in the table"


