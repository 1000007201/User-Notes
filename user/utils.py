import os
import jwt
import datetime
from dotenv import load_dotenv
load_dotenv()
from flask import request, jsonify
from functools import wraps


def get_token(user_name):
    token = jwt.encode({'User': user_name, 'Exp': str(datetime.datetime.utcnow() + datetime.timedelta(seconds=600))},
                       str(os.environ.get('SECRET_KEY')))
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'access-token' in request.headers:
            token = request.headers.get('access-token')
        else:
            token = request.args.get('token')
        if not token:
            return jsonify(message='Token is missing!')
        try:
            data = jwt.decode(token, str(os.environ.get('SECRET_KEY')), algorithms=["HS256"])
        except:
            return jsonify(message='Token is invalid')

        return f(data['User'])
    return decorated
