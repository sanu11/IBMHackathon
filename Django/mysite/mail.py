
import smtplib
toaddrs  = 'sanika.shah@ibm.com'
msg = 'Why,Oh why!'

username = "ibmhackathon89@gmail.com"
password = "ibmhackathon"
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(username, toaddrs, msg)
server.quit()
