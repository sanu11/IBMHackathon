MY_ADDRESS = "ibmhackathon@gmail.com"
PASSWORD = "ibmhackathon"
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
#    server.starttls()
#    server.login(MY_ADDRESS, PASSWORD)
except:
    print 'Something went wrong...'


