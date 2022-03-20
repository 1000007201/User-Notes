import json

from flask_restful import Resource
from flask import request, make_response, session, jsonify
from .validators import validate_add_notes, validate_add_label
from .utils import token_required
from .models import Notes


class AddNote(Resource):
    def post(self):
        if not session['logged_in']:
            return {'message': 'You have to login first'}
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
    def patch(self, topic):
        if not session['logged_in']:
            return {'Error': 'You have to login first'}
        try:
            note = Notes.objects(topic=topic)
        except Exception as e:
            return {'Error': str(e)}
        desc = request.form.get('Description')
        note.update(desc=desc)
        return {'message': 'Notes updated'}

    def delete(self, topic):
        if not session['logged_in']:
            return {'Error': 'You have to login first'}
        try:
            note = Notes.objects(topic=topic).first()
        except Exception as e:
            return {'Error': str(e)}
        note.delete()
        return {'message': 'Notes Deleted'}


class AddLabel(Resource):
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


class GetByLabel(Resource):
    def get(self, label):
        if not session['logged_in']:
            return {'Error': 'You have to login first'}
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
    @token_required
    def get(user_name):
        list_notes = []
        try:
            data_ = Notes.objects(user_name=user_name)
        except Exception as e:
            return {'Error': str(e)}
        for data in data_:
            dict_ = {'id': data.id, 'topic': data.topic, 'desc': data.desc, 'label': data.label}
            list_notes.append(dict_)

        return make_response(jsonify(list_notes), 200)
