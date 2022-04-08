from flask import session, request, json, make_response, jsonify
from flask_restful import Resource
from notes.models import Notes
from user.models import Users
from .models import Message
from middleware import auth
from common.utils import get_cache, do_cache
from common.custom_exceptions import NotFoundException, InternalServer


class SendMessage(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        """
        This Api adds new message
        :return: Response message after all validations
        """
        req_data = request.data
        body = json.loads(req_data)
        to_user = body.get('to_user')
        from_user = session['user_id']
        note_id = body.get('note_id')
        try:
            note = Notes.objects.filter(user_id=from_user, id=note_id).first()
            if not note:
                raise NotFoundException('Note not present', 404)
            msg = Message(from_user=from_user, to_user=to_user, note=note)
            msg.save()
        except NotFoundException as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': f'Notes are sent to {to_user}', 'code': 200}


class CheckMessage(Resource):
    method_decorators = {'get': [auth.login_required]}

    def get(self):
        """
        This Api returns all messages
        :return: list of notes messaged
        """
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
                     'notes': {'topic': data.note.topic,
                               'desc': data.note.desc,
                               'color': data.note.color,
                               'label': [lb.label for lb in data.note.label]}}
            list_all.append(dict_)
        key = f'message_{user_id}'
        do_cache(key, list_all, 30)
        print('data')
        return {'data': list_all, 'code': 200}


class GiveAccess(Resource):
    method_decorators = {'get': [auth.login_required]}

    def get(self, msg_id):
        """
        This Api adds user_id to contributors
        :param msg_id: ID of message having that note
        :return: Response message after all validations
        """
        try:
            msg = Message.objects.filter(id=msg_id).first()
            note_id = msg.note.id
            user_name = msg.to_user
            note = Notes.objects.filter(id=note_id).first()
            user = Users.objects.filter(user_name=user_name).first()
            note.update(push__contributors=user)
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': 'Access is given', 'code': 200}


class MessageNote(Resource):
    method_decorators = {'get': [auth.login_required]}

    def post(self, msg_id):
        """
        This Api make changes in message Note
        :param msg_id: ID of message
        :return: Response after all validations
        """
        try:
            msg = Message.objects.filter(id=msg_id).first()
            note_id = msg.note_id.id
            note = Notes.objects.filter(id=note_id).first()
            user_list = [nt.id for nt in note.contributors]
            if session['user_id'] not in user_list:
                raise InternalServer('You are not allowed to change note', 409)
            req_data = request.data
            body = json.loads(req_data)
            topic = body.get('topic')
            desc = body.get('desc')
            note.update(topic=topic, desc=desc)
        except InternalServer as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': 'Given note updated', 'code': 200}
