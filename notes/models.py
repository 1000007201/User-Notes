from mongoengine import Document, StringField, SequenceField, ListField, \
    ImageField, ReferenceField, PULL, URLField, IntField, BooleanField
from label import models
from user.models import Users

color_choices = ('red', 'green', 'blue', 'black')


class Notes(Document):
    id = SequenceField(primary_key=True)
    user_id = IntField()
    user_name = StringField(max_length=50)
    topic = StringField(max_length=100)
    desc = StringField(max_length=1000)
    color = StringField(choices=color_choices, default='black')
    image = ImageField()
    url = URLField()
    label = ListField(ReferenceField(models.Label, reverse_delete_rule=PULL))
    contributors = ListField(ReferenceField(Users, reverse_delete_rule=PULL))
    is_trash = BooleanField(default=False)
    is_pinned = BooleanField(default=False)
