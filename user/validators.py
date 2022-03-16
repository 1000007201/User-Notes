from .models import Users, Notes


def validate_registration(body):
    user_name = body.get('user_name')
    email = body.get('email')
    name = body.get('name')
    password = body.get('password')
    conf_password = body.get('conf_password')

    if not user_name and not email and not name:
        return {'Error': 'You have to enter all values!!!'}

    if not password == conf_password:
        return {'Error': 'confirm your password properly'}

    user = Users.objects(user_name=user_name)
    if user:
        return {'Error': 'Username already taken!!'}

    user_email = Users.objects(email=email)
    if user_email:
        return {'Error': 'Email already taken!!'}

    return {'data': body}


def validate_login(body):
    user_name = body.get('user_name')
    password = body.get('password')
    user = Users.objects(user_name=user_name, password=password)
    if not user:
        return {'Error': 'user_name not exist'}
    return {'data': body}


def validate_addnotes(body):
    topic = body.get('topic')
    desc = body.get('desc')
    if not topic or not desc:
        return {'Error': 'You have to fill both parameters'}
    note = Notes.objects(topic=topic)
    if note:
        return {'Error': 'Topic Already Exist'}
    return {'data': body}