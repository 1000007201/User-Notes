from mongoengine import Document, IntField, StringField, SequenceField


class Label(Document):
    id = SequenceField(primary_key=True)
    user_id = IntField()
    label = StringField(max_length=50)


