from flask_restful import Resource
from flask import request, make_response, session, json
from .validators import validate_registration, validate_login, validate_change_pass
from .utils import get_token, token_required
from .models import Users
from common import utils


class Registration(Resource):
    def post(self):
        req_data = request.data
        body = json.loads(req_data)
        validated_data = validate_registration(body)
        if validated_data:
            return make_response(validated_data, 409)
        del body['conf_password']
        data = Users(**body)
        data.save()
        token = get_token(data.user_name)
        short_token = utils.url_short(token)
        token_url = r"http://127.0.0.1:80/activate?token="+f"{short_token}"
        msg_text = f"Hello! {body['name']} click the link to activate your account {token_url}"
        utils.mail_sender(body['email'], msg_text)
        return {'message': 'User Added Check your registered mail id to activate account'}


class Login(Resource):
    def post(self):
        body = {}
        body['user_name'] = request.form.get('user_name')
        body['password'] = request.form.get('password')
        validate_data = validate_login(body)
        if 'Error' in validate_data:
            return make_response(validate_data, 409)
        if 'Error_active' in validate_data:
            token = get_token(body['user_name'])
            short_token = utils.url_short(token)
            token_url = r"http://127.0.0.1:80/activate?token="+f"{short_token}"
            msg_text = f"Hello! {body['name']} click the link to activate your account {token_url}"
            utils.mail_sender(body['email'], msg_text)
        token = get_token(body['user_name'])
        short_token = utils.url_short(token)
        session['logged_in'] = True
        session['user_name'] = body['user_name']
        return {'message': 'logged_in', 'token': short_token}


class ChangePass(Resource):
    def post(self):
        if session['logged_in']:
            req_data = request.data
            body = json.loads(req_data)
            validated_data = validate_change_pass(body)
            if validated_data:
                return make_response(validated_data, 409)
            else:
                user_name = session['user_name']
                new_pass1 = body.get('new_password')
                data_ = Users.objects.filter(user_name=user_name).first()
                data_.update(password=new_pass1)
                # logger.info(f'{user_name} changed his password')
                return {'message': 'Your Password is Updated.'}


class ForgetPass(Resource):
    def post(self):
        user_name = request.form.get('UserName')
        data_ = Users.objects(UserName=user_name).first()
        if not data_:
            return {'message': 'User name not found!!'}
        email = data_.Email
        name = data_.Name
        # logger.info(f'{user_name} has been forgotten his password')
        token = get_token(user_name)
        short_token = utils.url_short(token)
        token_url = r'http://127.0.0.1:80/setpass?token='+f'{short_token}'
        msg_text = f"Hello! {name} click the link to activate your account {token_url}"
        utils.mail_sender(email, msg_text)
        # logger.info(f'Mail is sent to registered mail id of user : {user_name} to set new password')
        return {'message': 'Check your Registered Mail ID to set new Password.'}


class Activate(Resource):
    @token_required
    def get(user_name):
        data = Users.objects.filter(user_name=user_name).first()
        data.update(is_active=True)
        # logger.info(f'User: {user_name} activated his account')

        return {'message': 'Your Account is Active.Now you can login'}


class SetPass(Resource):
    @token_required
    def post(user_name):
        data = Users.objects(UserName=user_name).first()
        password1 = request.form.get('new password')
        password2 = request.form.get('Re-Enter Password')
        if not password2 or not password1:
            return {'message': 'Password1 and Password2 can not be empty'}
        if password1 == password2:
            data.update(Password=password1)
            # logger.info(f'User: {user_name} has updated his password by forgot password')
            return {'message': 'Your Password is Set Now you can Login'}
        return {'message':'New Password and Re-Enter Password must be same'}


class LogOut(Resource):
    def get(self):
        session['logged_in'] = False
        return {'message': 'logged out'}
