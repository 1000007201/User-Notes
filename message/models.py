from mongoengine import Document, ReferenceField, CASCADE, SequenceField, IntField
from notes import models


class Message(Document):
    id = SequenceField(primary_key=True)
    from_user = IntField()
    to_user = IntField()
    note = ReferenceField(models.Notes, reverse_delete_rule=CASCADE)
