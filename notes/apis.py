import json
from flask_restful import Resource
from flask import request, make_response, session, jsonify
from .validators import validate_add_notes, validate_add_label
from .utils import token_required
from .models import Notes
from user import models
from middleware import auth


class AddNote(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        req_data = request.data
        body = json.loads(req_data)
        body['user_name'] = session['user_name']
        validated_data = validate_add_notes(body)
        if validated_data:
            return make_response(validated_data, 409)
        print(body)
        notes = Notes(**body)
        notes.save()
        return {'message': 'Notes Added'}


class NotesOperation(Resource):
    method_decorators = {'patch': [auth.login_required], 'delete': [auth.login_required]}

    def patch(self, id):
        try:
            note = Notes.objects(id=id)
        except Exception as e:
            return {'Error': str(e)}
        desc = request.form.get('Description')
        note.update(desc=desc)
        return {'message': 'Notes updated'}

    def delete(self, id):
        try:
            note = Notes.objects(id=id).first()
        except Exception as e:
            return {'Error': str(e)}
        note.delete()
        return {'message': 'Notes Deleted'}


class AddLabel(Resource):
    method_decorators = {'post': [auth.login_required], 'patch': [auth.login_required], 'delete': [auth.login_required]}

    def post(self, id):
        try:
            req_data = request.data
        except:
            return {'Error': 'Something went wrong'}
        body = json.loads(req_data)
        validate_data = validate_add_label(body)
        if validate_data:
            return {validate_data}
        label = body.get('label')
        try:
            note = Notes.objects.filter(user_name=session['user_name'], id=id).first()
            if not note:
                return {'Error': 'Note is not present'}
        except Exception as e:
            return {'Error': str(e)}
        note.update(push__label=label)
        return {'message': 'label added'}

    def patch(self, id):
        req_data = request.data
        body = json.loads(req_data)
        note = Notes.objects.filter(id=id, label=body.get('label')).first()
        if not note:
            return {'Error': 'label is not present in this note'}
        list_label = note.label
        list_label[list_label.index(body.get('label'))] = body.get('new_label')
        note.update(label=list_label)
        return {'message': 'label updated'}

    def delete(self, id):
        req_data = request.data
        body = json.loads(req_data)
        note = Notes.objects.filter(id=id, label=body.get('label')).first()
        if not note:
            return {'Error': 'label is not present in this note'}
        list_label = note.label
        list_label.remove(body.get('label'))
        note.update(label=list_label)
        return {'message': 'label removed'}


class GetByLabel(Resource):
    method_decorators = {'get': [auth.login_required]}

    def get(self, label):
        try:
            note = Notes.objects.filter(label=label)
        except Exception as e:
            return {'Error': str(e)}
        list_notes = []
        for data in note:
            dict_ = {'id': data.id, 'topic': data.topic, 'desc': data.desc, 'label': data.label}
            list_notes.append(dict_)
        return make_response(jsonify(list_notes), 200)


class Home(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, user_name):
        list_notes = []
        try:
            data_ = models.Users.objects.filter(user_name=user_name).first()
        except Exception as e:
            return {'Error': str(e)}
        if data_.is_super_user:
            dict_all = {}
            data_user = models.Users.objects()
            for data in data_user:
                note = Notes.objects.filter(user_name=data.user_name)
                list_user = []
                for itr in note:
                    dict_itr = {'id': itr.id, 'topic': itr.topic, 'desc': itr.desc, 'color': itr.color, 'label': itr.label}
                    list_user.append(dict_itr)
                dict_all[data.user_name] = list_user

            return make_response(dict_all)
        data_ = Notes.objects.filter(user_name=user_name).first()
        for data in data_:
            dict_ = {'id': data.id, 'topic': data.topic, 'desc': data.desc, 'label': data.label}
            list_notes.append(dict_)

        return make_response(jsonify(list_notes), 200)
