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

import logging
from datetime import datetime
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import mail

# email apis
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate



import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import  json
import base64

class Bimail:
    def __init__(self, subject, recipients):
        self.subject = subject
        self.recipients = recipients
        self.recipients = recipients
        self.htmlbody = ''
        self.sender = "mailsender135@gmail.com"
        self.senderpass = 'mailsender135.'
        self.attachments = []

    def send(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender
        msg['Subject'] = self.subject
        msg['To'] = ", ".join(self.recipients)  # to must be array of the form ['mailsender135@gmail.com']
        msg.preamble = "preamble goes here"
        # check if there are attachments if yes, add them
        if self.attachments:
            self.attach(msg)
        # add html body after attachments
        msg.attach(MIMEText(self.htmlbody, 'html'))
        # send
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.starttls()
        s.login(self.sender, self.senderpass)
        s.sendmail(self.sender, self.recipients, msg.as_string())
        # test
        print msg
        s.quit()

    def htmladd(self, html):
        self.htmlbody = self.htmlbody + '<p></p>' + html

    def attach(self, msg):
        for f in self.attachments:

            ctype, encoding = mimetypes.guess_type(f)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            if maintype == "text":
                fp = open(f)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(f, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(f, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(f, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=f)
            attachment.add_header('Content-ID', '<{}>'.format(f))
            msg.attach(attachment)

    def addattach(self, files):
        self.attachments = self.attachments + files










logger = logging.getLogger(__name__)
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


def get_login_page(request):
    return render(request,'scrum/login.html',{})


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
        # transcript.write(json.dumps(data, indent=2))
        transcript.write(data)

def storeRecordingToCloud(recording_path):
    logger.info("Inside cloud storage")
    # Constants for IBM COS values
    COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"  # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
    COS_API_KEY_ID = "8OzW_kP6cYhXmbGT2k4gDvD6su5PJc-3g3_zNc2WPPXD"  # eg "W00YiRnLW4a3fTjMB-oiB-2ySfTrFBIQQWanc--P3byk"
    COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
    COS_RESOURCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/f55b867e510248799db6fbb07b7693d0:9ffac231-7c90-4168-a8ab-2578b4c056b6::"  # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003abfb5d29761c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

    # Create resource

    cos = ibm_boto3.resource("s3",
                             ibm_api_key_id=COS_API_KEY_ID,
                             ibm_service_instance_id=COS_RESOURCE_CRN,
                             ibm_auth_endpoint=COS_AUTH_ENDPOINT,
                             config=Config(signature_version="oauth"),
                             endpoint_url=COS_ENDPOINT
                             )
    multi_part_upload(cos,"hackathon-recordings","recording.wav",recording_path)


def multi_part_upload(cos,bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))


def get_item(cos,bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        file = cos.Object(bucket_name, item_name).get()
        print("File Contents: {0}".format(file["Body"].read()))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))


def sendEmail():
    # toaddrs = 'sanika.shah@ibm.com'
    # msg = 'Why,Oh why sanika!'
    #
    # username = "ibmhackathon89@gmail.com"
    # password = "ibmhackathon"
    # server = smtplib.SMTP('smtp.gmail.com:587')
    # server.starttls()
    # server.login(username, password)
    # server.sendmail(username, toaddrs, msg)
    # server.quit()
    email = Bimail('Sales email ' +datetime.now().strftime('%Y/%m/%d'), ['sanika.shah@ibm.com', 'ryan.kelly@ibm.com'])
    email.send()

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
            storeRecordingToCloud('/static/recording.wav')
            sendEmail()

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
    logger.debug("ibm watson called!")
    writeToFile("sanika sHsah sanika shaha sanika shaha")
    storeRecordingToCloud('/static/recording.wav')
    sendEmail()
    return render(request,'scrum/recording.html',{"recording":"/static/recording.wav","name":"recording.wav"})

def main(request):
    return render(request, 'scrum/index.html', {})

def saveRecording(request):
    print "saved recording to bluemix and the path in the table"


