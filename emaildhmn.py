import argparse
import os
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64

def sendMail(u,p,r,subject, text, *attachmentFilePaths):
  gmailUser = u
  gmailPassword = p
  recipient = r

  msg = MIMEMultipart()
  msg['From'] = gmailUser
  msg['To'] = recipient
  msg['Subject'] = subject
  msg.attach(MIMEText(text))

  for attachmentFilePath in attachmentFilePaths:
    msg.attach(getAttachment(attachmentFilePath))

  mailServer = smtplib.SMTP('smtp.gmail.com', 587)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(gmailUser, gmailPassword)
  mailServer.sendmail(gmailUser, recipient, msg.as_string())
  mailServer.close()

def getAttachment(attachmentFilePath):
  contentType, encoding = mimetypes.guess_type(attachmentFilePath)

  if contentType is None or encoding is not None:
    contentType = 'application/octet-stream'

  mainType, subType = contentType.split('/', 1)
  file = open(attachmentFilePath, 'rb')

  if mainType == 'text':
    attachment = MIMEText(file.read())
  elif mainType == 'message':
    attachment = email.message_from_file(file)
  elif mainType == 'image':
    attachment = MIMEImage(file.read(),_subType=subType)
  elif mainType == 'audio':
    attachment = MIMEAudio(file.read(),_subType=subType)
  else:
    attachment = MIMEBase(mainType, subType)
  attachment.set_payload(file.read())
  encode_base64(attachment)

  file.close()

  attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachmentFilePath))
  return attachment

harmony = """
Open Hack-n-Make!     
Thursday 6pm-10pm     
Harmony Cafe 3rd Floor
233 E College Ave     
Appleton, WI 54911    
"""

lunch = """
Makers Lunch Meetup!   
Friday 11:30am-1:30pm
Hong Kong Buffet       
145 W Wisconsin Ave    
Neenah, WI 54956       
"""

orgmeeting = """
Open Organizational Meeting
Monday 8pm-10pm          
Cambria Suites Hotel Lobby 
3940 North Gateway Drive   
Appleton, WI 54913         
"""

footer = """
--                               
Recurring Monthly Events:        
* Hack/Make Meetup 1st Thursdays 
* Makers Lunch Meetup 2nd Fridays
* Hack/Make Meetup 3rd Thursdays 
* Org Meeting 4th Mondays        
"""

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Send weekly events to dhmn-discuss.')
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    parser.add_argument('recipient')
    args = parser.parse_args()

    import datetime
    d = datetime.date.today()
    mon = d.day #cron runs every monday
    thu = (d + datetime.timedelta(days=3)).day
    fri = (d + datetime.timedelta(days=4)).day
    if mon > 21 and mon < 29: sendMail(args.user,args.password,args.recipient,"This Week - Org Meeting(4th Monday)",orgmeeting + footer)
    if thu > 0  and thu <  8: sendMail(args.user,args.password,args.recipient,"This Week - Hack/Make Meetup(1st Thursday)",harmony + footer)
    if thu > 14 and thu < 22: sendMail(args.user,args.password,args.recipient,"This Week - Hack/Make Meetup(3rd Thursday)",harmony + footer)
    if fri > 7  and fri < 15: sendMail(args.user,args.password,args.recipient,"This Week - Lunch Meetup(2nd Friday)",lunch + footer)

