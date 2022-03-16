from mongoengine import Document, StringField, EmailField, DateTimeField
import datetime


class Users(Document):
    user_name = StringField(max_length=50, unique=True)
    name = StringField(max_length=50)
    email = EmailField(unique=True)
    password = StringField()
    dt_created = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        user_dict={
            'user_name': self.user_name,
            'name': self.name,
            'email': self.email,
            'dt_created': self.dt_created
        }
        return user_dict


class Notes(Document):
    user_name = StringField(max_length=50)
    topic = StringField(max_length=100)
    desc = StringField(max_length=1000)

    def to_dict(self):
        notes_dict = {
            'user_name': self.user_name,
            'topic': self.topic,
            'desc': self.desc
        }
        return notes_dict
