from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField
import datetime


class Users(Document):
    user_name = StringField(max_length=50, unique=True)
    name = StringField(max_length=50)
    email = EmailField(unique=True)
    password = StringField()
    is_active = BooleanField(default=False)
    is_super_user = BooleanField(default=False)
    dt_created = DateTimeField(default=datetime.datetime.now)
