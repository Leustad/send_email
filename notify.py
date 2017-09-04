import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sys


def notify_by_email():
    COMMASPACE = ', '

    HOST = '<HOES URL GOES HERE>'
    SENDER = 'SENDER@SENDER.COM'
    RECIPIENTS = ['RECEIVER1@RECEIVER.COM', 'RECEIVER2@RECEIVER.COM']
    TEXT = '<TEXT BODY GOES HERE>\n\n\n\n'

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = '<SUBJECT LINE GOES HERE>'
    outer['To'] = COMMASPACE.join(RECIPIENTS)
    outer['From'] = SENDER
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    outer.attach(MIMEText(TEXT))

    # Attachments
    attachment = '<ATTACH_FILE/PATH/>'

    try:
        with open(attachment, 'rb') as fp:
            msg = MIMEBase('application', "octet-stream")
            msg.set_payload(fp.read())
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
        outer.attach(msg)

    except:
        print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
        raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP(HOST) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.sendmail(SENDER, RECIPIENTS, composed)
            s.close()
        print("\nEmail sent!")
    except:
        print("\nUnable to send the email. Error: ", sys.exc_info()[0])
        raise
