from flask_restful import Resource
from flask import request, make_response, session, json, render_template
from flask.views import MethodView
from .validators import validate_registration, validate_login, validate_change_pass
from .utils import get_token, token_required
from .models import Users
from common import utils
from middleware import auth
from common import custome_logger
from task import mail_sender
from common.custom_exceptions import NullValueException, NotFoundException


class Registration(Resource):
    def post(self):
        req_data = request.data
        body = json.loads(req_data)
        validated_data = validate_registration(body)
        if validated_data:
            return make_response(validated_data, 409)
        del body['conf_password']
        try:
            data = Users(**body)
            data.save()
            custome_logger.logger.info(f'New user is added of username: {data.user_name}')
            token = get_token(data.id)
            short_token = utils.token_short(token)
            token_url = r"http://127.0.0.1:80/activate?token="+f"{short_token}"
            template = render_template('index.html', data=token_url)
            mail_sender.delay(template, body['email'])
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        custome_logger.logger.info(f'Mail sent for activation of account to registered mail id of User: {data.user_name}')
        return {'message': 'User Added Check your registered mail id to activate account', 'code': 200}


class Login(Resource):
    def post(self):
        body = {}
        body['user_name'] = request.form.get('user_name')
        body['password'] = request.form.get('password')
        validate_data = validate_login(body)
        if 'Error' in validate_data:
            return {'data': validate_data}
        if 'Error_active' in validate_data:
            token = get_token(validate_data['user_id'])
            short_token = utils.token_short(token)
            token_url = r"http://127.0.0.1:80/activate?token="+f"{short_token}"
            template = render_template('index.html', data=token_url)
            mail_sender.delay(template, validate_data['email'])
            return {'message': 'Your account is not active activate it before login and for activation check your '
                               'mail id', 'code': 200}
        token = get_token(validate_data['user_id'])
        short_token = utils.token_short(token)
        session.clear()
        session['logged_in'] = True
        session['user_id'] = validate_data['user_id']
        custome_logger.logger.info(f'User: {body["user_name"]} logged in')
        return {'message': 'logged_in', 'token': short_token, 'code': 200}


class ChangePass(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        req_data = request.data
        body = json.loads(req_data)
        validated_data = validate_change_pass(body)
        if validated_data:
            return {'data': validated_data, 'code': 404}
        else:
            user_id = session['user_id']
            new_pass1 = body.get('new_password')
            try:
                data_ = Users.objects.filter(id=user_id).first()
                data_.update(password=new_pass1)
            except Exception as e:
                return {'Error': str(e), 'code': 500}
            custome_logger.logger.info(f'User_id:{user_id} changed his password')
            return {'message': 'Your Password is Updated', 'code': 200}


class ForgetPass(Resource):
    def post(self):
        user_id = request.form.get('user_id')
        try:
            data_ = Users.objects.filter(id=user_id).first()
            if not data_:
                raise NotFoundException('User not found!!', 404)
            email = data_.Email
            custome_logger.logger.info(f'User_id:{user_id} has been forgotten his password')
            token = get_token(user_id)
            short_token = utils.token_short(token)
            token_url = r'http://127.0.0.1:80/setpass?token='+f'{short_token}'
            template = render_template('forget.html', data=token_url)
            mail_sender.delay(template, email)
        except NotFoundException as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        custome_logger.logger.info(f'Mail is sent to registered mail id of user_id : {user_id} to set new password')
        return {'message': 'Check your Registered Mail ID to set new Password.', 'code': 200}


class ActivateView(MethodView):
    decorators = [token_required]

    def get(self, user_id):
        try:
            data = Users.objects.filter(id=user_id).first()
            data.update(is_active=True)
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        custome_logger.logger.info(f'User_id: {user_id} activated his account')
        data = {'message': 'Your Account is Active.Now you can login'}
        return render_template('activate.html', data=data)


class SetPass(Resource):
    method_decorators = {'post': [token_required]}

    def post(self, user_id):
        password1 = request.form.get('new password')
        password2 = request.form.get('Re-Enter Password')
        try:
            data = Users.objects(id=user_id).first()
            if not password2 or not password1:
                raise NullValueException('Password1 and Password2 can not be empty', 409)
            if password1 != password2:
                raise NullValueException('New Password and Re-Enter Password must be same', 409)
            if password1 == password2:
                data.update(Password=password1)
        except NullValueException as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        custome_logger.logger.info(f'User_id: {user_id} has updated his password by forgot password')
        return {'message': 'Your Password is Set Now you can Login', 'code': 200}


class LogOut(Resource):
    def get(self):
        session.clear()
        custome_logger.logger.info(f'logged out')
        return {'message': 'logged out'}
