from flask_restful import Resource
from flask import request, make_response, session, jsonify
from .validators import validate_registration, validate_login, validate_addnotes
from .utils import token_required, get_token
from .models import Users, Notes


class Registration(Resource):
    def post(self):
        body = {}
        body['user_name'] = request.form.get('user_name')
        body['name'] = request.form.get('name')
        body['email'] = request.form.get('email')
        body['password'] = request.form.get('password')
        body['conf_password'] = request.form.get('Confirm Password')
        validated_data = validate_registration(body)
        if 'Error' in validated_data:
            return make_response(validated_data, 409)
        del body['conf_password']
        data = Users(**validated_data['data'])
        data.save()
        return {'message': 'User Added'}


class Login(Resource):
    def post(self):
        body = {}
        body['user_name'] = request.form.get('user_name')
        body['password'] = request.form.get('password')
        validate_data = validate_login(body)
        if 'Error' in validate_data:
            return make_response(validate_data, 409)
        print(type(body['user_name']))
        token = get_token(body['user_name'])
        session['logged_in'] = True
        session['user_name'] = body['user_name']
        return {'message': 'logged_in', 'token': token}


class LogOut(Resource):
    def get(self):
        session['logged_in'] = False
        return {'message': 'logged out'}


class AddNote(Resource):
    def post(self):
        body = {}
        if not session['logged_in']:
            return {'message': 'You have to login first'}
        body['user_name'] = session['user_name']
        body['topic'] = request.form.get('Topic')
        body['desc'] = request.form.get('Description')
        validated_data = validate_addnotes(body)
        if 'Error' in validated_data:
            return make_response(validated_data, 409)
        notes = Notes(**body)
        notes.save()
        return {'message': 'Notes Added'}


class Home(Resource):
    @token_required
    def get(user_name):
        list_notes = []
        data_ = Notes.objects(user_name=user_name)

        for data in data_:
            dict_ = {}
            dict_['topic'] = data.topic
            dict_['desc'] = data.desc
            list_notes.append(dict_)

        return make_response(jsonify(list_notes), 200)


class NotesOperation(Resource):
    def patch(self, topic):
        if not session['logged_in']:
            return {'Error': 'You have to login first'}
        note = Notes.objects(topic=topic)
        desc = request.form.get('Description')
        note.update(desc=desc)
        return {'message': 'Notes updated'}

    def delete(self, topic):
        if not session['logged_in']:
            return {'Error': 'You have to login first'}
        note = Notes.objects(topic=topic).first()
        note.delete()
        return {'message': 'Notes Deleted'}


