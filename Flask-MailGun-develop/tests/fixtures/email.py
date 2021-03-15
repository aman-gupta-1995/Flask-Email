# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:30:28 2016

@author: richard
"""
from flask import Request
import hashlib
import hmac
import random
import string
from time import time
from tests.fixtures import get_attachment
from flask_mailgun.message import Message

url_safe_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits


def random_string(length):
    return ''.join(random.choice(url_safe_chars) for i in range(length))


def sign_email(email, mailgun):
    token = random_string(50)
    timestamp = int(time())
    api_key = mailgun.mailgun_api.api_key
    message = '{}{}'.format(timestamp, token).encode('utf-8')
                                 
    signature = hmac.new(key=api_key,
                         msg=message,
                         digestmod=hashlib.sha256).hexdigest()
    email.update(dict(token=token,
                      timestamp=timestamp,
                      signature=signature))
    return email


def make_email():
    """factory for making a email test fixture"""
    # calculate the email signature as in
    # https://documentation.mailgun.com/user_manual.html#webhooks
    email = {"sender": "test@testy.mc.testface",
             "from": "test@testy.mc.testface",
             "recipient": ["user1@example.com", "user2@example.com"],
             "subject": "Hello",
             "body-plain": "Testing some Mailgun awesomness!"}
    return email


def attach_file(email):
    """generate request with attachment"""
    (filename, file_stream) = get_attachment()
    attachment = dict(filename=filename,
                      file=file_stream)
    email.update({"attachment-count": 1})
    # generate request
    email.update({'attachment-1': attachment})
    return email


def make_email_request(mailgun):
    email = make_email()
    email = sign_email(email, mailgun)
    return attach_file(email)
