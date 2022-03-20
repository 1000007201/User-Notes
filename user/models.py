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

    def to_dict(self):
        user_dict = {
            'user_name': self.user_name,
            'name': self.name,
            'email': self.email,
            'dt_created': self.dt_created
        }
        return user_dict
