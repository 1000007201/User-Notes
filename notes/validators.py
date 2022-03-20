from .models import Notes
from flask import session


def validate_add_notes(body):
    topic = body.get('topic')
    desc = body.get('desc')
    if not desc or not topic:
        return {'Error': 'You have to fill both parameters'}


def validate_add_label(body):
    if not session['logged_in']:
        return {'Error': 'You have to login first'}
    label = body.get('label')
    if not label:
        return {'Error': 'Label can not be null'}
