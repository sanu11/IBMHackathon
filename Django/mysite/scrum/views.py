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
import parse
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

from django.contrib.auth.models import User
from django.db.utils import IntegrityError

class Bimail:
    def __init__(self, subject, recipients):
        self.subject = subject
        self.recipients = recipients
        self.recipients = recipients
        self.htmlbody = ''
        self.sender = "ibmhackathon89@gmail.com"
        self.senderpass = 'ibmhackathon'
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


def login_check(request):
    data = json.loads(request.body)
    username=data["username"]
    password = data["password"]
    if Team.objects.filter(name=username).exists():
        obj = Team.objects.get(name=username)
        if check_password(password, obj.password):
            print username, password
            request.session['team_name'] = obj.team_name
            return HttpResponse("Success")
        else:
            return HttpResponse("Incorrect Password")
    else:
        return HttpResponse("User doesn't exists")

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
    path=SITE_ROOT+'/static/recording.mp3'
    with open(path, 'w+') as output:
        output.write(audiofile_byte)

    # with tempfile.TemporaryFile(mode='w') as f:
    #     audiofile_byte.write_to_fp(f)
    #     file_name = '{}.wav'.format(file_name)
    #     audiofile_byte.save(file_name, File(file=f))

    # file_name = default_storage.save(file_name, file)

    return HttpResponse("Success")


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
    multi_part_upload(cos,"hackathon-recordings","recording.mp3",recording_path)


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
    email_receipents =  ['sanika.shah@ibm.com','pooja.patel1@ibm.com','ryan.kelly@ibm.com','huan.wu@ibm.com','kishan.agarwal@ibm.com','manjari.subramani@ibm.com']
    email = Bimail('Sales email ' +datetime.now().strftime('%Y/%m/%d'), email_receipents)
    email.send()


def watson():
    path = SITE_ROOT + '/static'
    path2 = SITE_ROOT+'/static'
    parse.parse_audio(path)
    # con_file=parse.convert()
    # with open(path2+'/recording.txt') as f:
    #     for i in con_file:
    #         f.write(i+"\n")

@csrf_exempt
def get_register_page(request):
    return render(request,'scrum/register.html',{})

@csrf_exempt
def createSuperUser(request):
    User.objects.create_superuser(username='admin', password='admin', email='sanika.shah@ibm.com')
    return HttpResponse("Admin User created locally")


@csrf_exempt
def playRecording(request):
    path=SITE_ROOT+'/static/recording.mp3'
    watson()
    print "called ibm watson"
    storeRecordingToCloud(path)
    print "stored data to file"
    sendEmail()
    print "email sent"
    return render(request,'scrum/home.html',{"recording":"/static/recording.mp3","name":"recording.mp3"})

def main(request):
    return render(request, 'scrum/home.html', {})

def saveRecording(request):
    print "saved recording to bluemix and the path in the table"

