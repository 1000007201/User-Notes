from mongoengine import connect


def connect_db():
    connect(host='mongodb://localhost/Notes')