---
date: 2017-08-30 00:00:27.580816
layout: post
title: Gmail & Outlook Thread Creator
description: "email_generator"
tags: [python]
comments: true
---

This is a demo of email thread generator based from Gmail to Gmail and Outlook. It can 

* Send N email with different titles.<br/>
* Create an email thread with N conversations (i.e. grouping N emails
   together).<br/>

Prerequisite:

* Check out [Gmail API quickstart](https://developers.google.com/gmail/api/quickstart/python) to authorize API usage and save the private key file *client_secret.json* in your working directory.


<!--excerpt-->

Syntax:
{% highlight python %}
#create 5 emails all with different title
python sender.py --to youralias@gmail.com --num_threads 5 
{% endhighlight %}

{% highlight python %}
#create 10 emails in the same thread
python sender.py --to youralias@gmail.com --num_conversations 10 
{% endhighlight %}

Since Outlook classifies emails a little different, to make the conversational thread work, a user needs to copy to message ID from the first email. Command line message will provide a step by step guide.

{% highlight python %}
# sender.py
import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def SendMessage(sender, to, subject, msgHtml, msgPlain, msgId='', threadId=''):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = CreateMessage(sender, to, subject, msgHtml, msgPlain, msgId, threadId)
    return SendMessageInternal(service, "me", message1)

def SendMessageInternal(service, user_id, message):
    ''' if success, return threadID, else return None'''
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Thread Id: %s' % message['id'])
        return message['id'] 
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None

def CreateMessage(sender, to, subject, msgHtml, msgPlain, msgId, threadId):
    '''threadId: for gmail; msgId: for Outlook'''
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    if msgId:
        msg['In-Reply-To'] = msgId
        msg['References'] = msgId
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    if threadId:
        body['threadId'] = threadId  
    return body

def CreateConversations(sender, to, subject, msgHtml, msgPlain, msgId, threadId, num):
    for i in range(num):
        # retry until success
        success = False
        while not success:
            success = SendMessage(sender, to, subject, msgHtml, msgPlain, msgId, threadId)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--to', type=str, default='foobarplay@gmail.com')
    parser.add_argument('--title', type=str, help='email title', default='Thread')
    parser.add_argument('--num_threads', type=int, help='num_threads', default=1)
    parser.add_argument('--num_conversations', type=int, help='num conversations of a thread (thread ID required)', default=1)
    args = parser.parse_args()                

    # create first mail, get msg id
    to = args.to
    sender = "youralias@gmail.com"
    msgHtml, msgPlain= "bar", "foo"
    is_gmail = 'gmail' in args.to

    for i in range(args.num_threads):
        subject = args.title + (str(i) if i>0 else '')
        # retry until success
        Id = None
        while not Id:
            Id = SendMessage(sender, to, subject, msgHtml, msgPlain)

    threadId, msgId = '', ''
    if args.num_conversations > 1:
        if is_gmail:
            threadId = Id
        else:
            msgId = input('Please check the latest mail and insert its msgId (e.g. <CAFi=xyz@mail.gmail.com>):')
        CreateConversations(sender, to, subject, msgHtml, msgPlain, msgId, threadId, args.num_conversations-1)
        print('Conversations created to the given thread')
{% endhighlight %}


