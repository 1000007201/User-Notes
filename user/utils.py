import os
import jwt
import datetime
from dotenv import load_dotenv
load_dotenv()
from flask import request, jsonify
from functools import wraps
from common import utils


def get_token(user_id):
    token = jwt.encode({'User_id': user_id, 'Exp': str(datetime.datetime.utcnow() + datetime.timedelta(seconds=600))},
                       str(os.environ.get('SECRET_KEY')))
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'access-token' in request.headers:
            short_token = request.headers.get('access-token')
        else:
            short_token = request.args.get('token')
        token = utils.true_token(short_token)
        if not token:
            return {'message':'Token is missing!', 'code': 409}
        try:
            data = jwt.decode(token, str(os.environ.get('SECRET_KEY')), algorithms=["HS256"])
        except:
            return {'message':'Token is invalid', 'code': 409}

        return f(data['User_id'])
    return decorated
