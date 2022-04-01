from flask import session, request, json, make_response, jsonify
from flask_restful import Resource
from notes.models import Notes
from user.models import Users
from .models import Message
from middleware import auth
from common.utils import get_cache, do_cache


class SendMessage(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        req_data = request.data
        body = json.loads(req_data)
        to_user = body.get('to_user')
        from_user = session['user_id']
        note_id = body.get('note_id')
        note = Notes.objects.filter(user_id=from_user, id=note_id).first()
        if not note:
            return {'Error': 'Note not present', 'code': 500}
        msg = Message(from_user=from_user, to_user=to_user, note=note)
        msg.save()
        return {'message': f'Notes are sent to {to_user}', 'code': 200}


class CheckMessage(Resource):
    method_decorators = {'get': [auth.login_required]}

    def get(self):
        user_id = session['user_id']
        key = f'message_{user_id}'
        value = get_cache(key)
        if value:
            _data = json.loads(value)
            print('red')
            return {'data': _data}

        msg = Message.objects.filter(to_user=user_id)
        if not msg:
            return {'message': 'No notes are shared with you', 'code': 500}
        list_all = []
        for data in msg:
            dict_ = {'from': data.from_user,
                     'notes': {'topic': data.note_id.topic,
                               'desc': data.note_id.desc,
                               'color': data.note_id.color,
                               'label': [lb.label for lb in data.note_id.label]}}
            list_all.append(dict_)
        key = f'message_{user_id}'
        do_cache(key, list_all, 30)
        print('data')
        return {'data': list_all, 'code': 200}


class GiveAccess(Resource):
    method_decorators = {'get': [auth.login_required]}

    def get(self, msg_id):
        msg = Message.objects.filter(id=msg_id).first()
        note_id = msg.note.id
        user_name = msg.to_user
        note = Notes.objects.filter(id=note_id).first()
        user = Users.objects.filter(user_name=user_name).first()
        note.update(push__contributors=user)
        return {'message': 'Access is given', 'code': 200}


class MessageNote(Resource):
    method_decorators = {'get': [auth.login_required]}

    def post(self, msg_id):
        msg = Message.objects.filter(id=msg_id).first()
        note_id = msg.note_id.id
        note = Notes.objects.filter(id=note_id).first()
        user_list = [nt.id for nt in note.contributors]
        if session['user_id'] not in user_list:
            return {'Error': 'You are not allowed to change note', 'code': 409}
        req_data = request.data
        body = json.loads(req_data)
        topic = body.get('topic')
        desc = body.get('desc')
        note.update(topic=topic, desc=desc)
        return {'message': 'Given note updated', 'code': 200}
