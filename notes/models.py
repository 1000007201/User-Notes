from mongoengine import Document, StringField, SequenceField, ListField

color_choices = ('red', 'green', 'blue', 'black')


class Notes(Document):
    id = SequenceField(primary_key=True)
    user_name = StringField(max_length=50)
    topic = StringField(max_length=100)
    desc = StringField(max_length=1000)
    color = StringField(choices=color_choices, default='black')
    label = ListField(StringField(max_length=50))
