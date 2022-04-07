from .models import Users
from flask import session
from common.custom_exceptions import NullValueException, AlreadyExistException, NotFoundException


def validate_registration(body):
    user_name = body.get('user_name')
    email = body.get('email')
    name = body.get('name')
    password = body.get('password')
    conf_password = body.get('conf_password')

    try:
        if not user_name and not email and not name:
            raise NullValueException('You have to enter all values', 404)

        if not password == conf_password:
            raise NullValueException('confirm your password properly', 404)

        user = Users.objects(user_name=user_name)
        if user:
            raise AlreadyExistException('Username already taken!!', 404)

        user_email = Users.objects(email=email)
        if user_email:
            raise AlreadyExistException('Email already taken!!', 404)

    except AlreadyExistException as exception:
        return exception.__dict__

    except NullValueException as exception:
        return exception.__dict__


def validate_login(body):
    try:
        user_name = body.get('user_name')
        password = body.get('password')
        # if session['logged_in'] and session['user_name'] == body['user_name']:
        #     return {'Error': 'You are already logged in'}
        data_ = Users.objects(user_name=user_name, password=password).first()
        if not data_:
            raise NotFoundException('user_name not exist', 404)
        if not data_.is_active:
            return {'Error_active': 'your account is not activate yet check your registered mail id to activate account',
                    'email': f'{data_.email}', 'user_id': data_.id}
        return {'data': body, 'user_id': data_.id}
    except NotFoundException as exception:
        return exception.__dict__
    except Exception as e:
        return {'Error': str(e), 'code': 500}


def validate_change_pass(body):
    try:
        user_id = session['user_id']
        old_pass = body.get('old_password')
        new_pass1 = body.get('new_password')
        new_pass2 = body.get('Re-Enter new_password')
        if new_pass1 != new_pass2:
            raise NullValueException('You have to re-enter password correctly', 409)

        data_ = Users.objects.filter(id=user_id).first()
        if data_.password != old_pass:
            raise NullValueException('You have to enter right old password', 409)
    except NullValueException as exception:
        return exception.__dict__
    except Exception as e:
        return {'Error': str(e), 'code': 500}
