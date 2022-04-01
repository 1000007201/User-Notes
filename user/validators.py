from .models import Users
from flask import session


def validate_registration(body):
    user_name = body.get('user_name')
    email = body.get('email')
    name = body.get('name')
    password = body.get('password')
    conf_password = body.get('conf_password')

    if not user_name and not email and not name:
        return {'Error': 'You have to enter all values!!!', 'code': 409}

    if not password == conf_password:
        return {'Error': 'confirm your password properly', 'code': 409}

    user = Users.objects(user_name=user_name)
    if user:
        return {'Error': 'Username already taken!!', 'code': 404}

    user_email = Users.objects(email=email)
    if user_email:
        return {'Error': 'Email already taken!!', 'code': 409}


def validate_login(body):
    user_name = body.get('user_name')
    password = body.get('password')
    if session['logged_in'] and session['user_name'] == body['user_name']:
        return {'Error': 'You are already logged in'}
    # if session['logged_in'] and session['user_name'] != body['user_name']:
    #     return {'Error': 'Another user is logged in'}
    data_ = Users.objects(user_name=user_name, password=password).first()
    if not data_:
        return {'Error': 'user_name not exist'}
    if not data_.is_active:
        return {'Error_active': 'your account is not activate yet check your registered mail id to activate account',
                'email': f'{data_.email}', 'user_id': data_.id}
    return {'data': body, 'user_id': data_.id}


def validate_change_pass(body):
    user_id = session['user_id']
    old_pass = body.get('old_password')
    new_pass1 = body.get('new_password')
    new_pass2 = body.get('Re-Enter new_password')
    if new_pass1 != new_pass2:
        return {'Error': 'You have to re-enter password correctly'}

    data_ = Users.objects.filter(id=user_id).first()
    if data_.password != old_pass:
        return {'Error': 'You have to enter right old password'}
