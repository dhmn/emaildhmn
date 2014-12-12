"""
Copyright (c) 2012 Mike Putnam <mike@theputnams.net>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

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

"""
Based on http://codecomments.wordpress.com/2008/01/04/python-gmail-smtp-example/

Added argparse bits to move gmail credentials out of the script.
Hardcoded the schedule and messages into the script.
"""

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

hackmakes = """
- Open Make Session! Thursday 6:00pm-10:00pm     
- Open Make Session - Saturdays till year end! 12:00pm-5:00pm (approx.)
"""

newlugmeeting = """
- NEWLUG Linux Users Group Meeting! Tuesday 6:30pm-9:00pm
"""

orgmeeting = """
- Open Organizational Meeting! Monday 8:00pm
"""

footer = """

--                               
Recurring Weekly Events:
* Public - Open Make Session every Thursday
* Members - Art/Music night Friday

Recurring Monthly Events:        
* Public - NEWLUG Meeting 2nd Tuesdays
* Public - Org Meeting 4th Mondays

Want a place to track your project, or look at what others are working on?  Check out the Trello Project Board!
https://trello.com/b/eSPKdh9O/dhmn-project-board

Appleton Makerspace
121R B North Douglas St
Appleton, WI 54914
"""

projects = """
Makers! It's time to share... what have you been hacking on or making?

Reply to this email with a brief run-down of whatever projects have been keeping you busy.


*** This weekly sharing encouragement idea shamelessly stolen from reMMinderbot at Milwaukee Makerspace http://groups.google.com/group/milwaukeemakerspace
"""

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Send weekly events to dhmn-discuss.')
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    parser.add_argument('recipient')
    args = parser.parse_args()

    import datetime
    d = datetime.date.today()
    datestring = '{0:04d}-{1:02d}-{2:02d}'.format(d.year, d.month, d.day)
    mon = d.day #cron runs every monday
    fri = (d + datetime.timedelta(days=4)).day
    this_week_email_body = ""
    if mon > 7  and mon < 15: this_week_email_body += newlugmeeting) #2nd week
    if mon > 21 and mon < 29: this_week_email_body += orgmeeting) #4th week
    sendMail(args.user,args.password,args.recipient,"This Week at the Appleton Makerspace",this_week_email_body + hackmakes + footer) # every week
    sendMail(args.user,args.password,args.recipient,"What Have You Been Hacking/Making? ["+datestring+" edition]",projects) #every week
