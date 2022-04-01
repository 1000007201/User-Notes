import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import base64
from dotenv import load_dotenv
import redis
load_dotenv()

r = redis.Redis(
    host='localhost',
    port=6379
)


def mail_sender(bodyContent, email):
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = MIMEMultipart()
    msg['Subject'] = 'Activate Account'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.attach(MIMEText(bodyContent, "html"))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(msg)


def token_short(token):
    token_string_bytes = token.encode("ascii")

    base64_bytes = base64.b64encode(token_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def true_token(token_):
    base64_bytes = token_.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")

    return sample_string


def do_cache(key, value, expire_time):
    json_dict = json.dumps(value)
    r.set(key, json_dict)
    r.expire(key, expire_time)


def get_cache(key):
    value = r.get(key)
    return value
