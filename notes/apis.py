from flask_restful import Resource
from flask import request, make_response, session, jsonify, json
from .validators import validate_add_notes, validate_add_label
from .utils import token_required
from .models import Notes
from label import models as md
from user import models
from middleware import auth
from common import custome_logger


class AddNote(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        body = {}
        req_data = request.data
        body = json.loads(req_data)
        # image_ = request.files['image']
        body['user_name'] = session['user_name']
        validated_data = validate_add_notes(body)
        if validated_data:
            return make_response(validated_data, 409)
        notes = Notes(**body)
        # notes.image.replace(image_, filename='my_image')
        notes.save()
        custome_logger.logger.info(f'Notes added by User: {notes.user_name}')
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
        custome_logger.logger.info(f'Notes are updated of id:{id} by User: {session["user_name"]}')
        return {'message': 'Notes updated'}

    def delete(self, id):
        try:
            note = Notes.objects(id=id).first()
        except Exception as e:
            return {'Error': str(e)}
        note.delete()
        custome_logger.logger.info(f'Notes are deleted of id:{id} by User: {session["user_name"]}')
        return {'message': 'Notes Deleted'}


class NoteLabel(Resource):
    method_decorators = {'post': [auth.login_required], 'patch': [auth.login_required], 'delete': [auth.login_required]}

    def post(self, id):
        req_data = request.data
        body = json.loads(req_data)
        validate_data = validate_add_label(body)
        if validate_data:
            return {validate_data}
        label = body.get('label')
        user_name = session['user_name']
        label_data = md.Label.objects.filter(user_name=user_name, label=label).first()
        if not label_data:
            label_data = md.Label(user_name=user_name, label=label)
            label_data.save()
        try:
            note = Notes.objects.filter(user_name=session['user_name'], id=id).first()
            if not note:
                return {'Error': 'Note is not present'}
        except Exception as e:
            return {'Error': str(e)}
        for data in note.label:
            if data.label == label:
                return {'Error': 'label already present in this note'}
        note.update(push__label=label_data)
        custome_logger.logger.info(f'Label is added to notes of id:{id} by User: {session["user_name"]}')
        return {'message': 'label added'}

    def patch(self, id):
        req_data = request.data
        body = json.loads(req_data)
        old_label = body.get('label')
        new_label = body.get('new_label')
        user_name = session['user_name']
        note = Notes.objects.filter(id=id, user_name=user_name).first()
        label2 = md.Label.objects.filter(user_name=user_name, label=new_label).first()
        if not label2:
            label2 = md.Label(user_name=user_name, label=new_label)
            label2.save()
        label_list = note.label
        for i in label_list:
            if i.label == old_label:
                label_list.remove(i)
                label_list.append(label2)
                note.update(label=label_list)
                custome_logger.logger.info(f'Label is updated of notes of id:{id} by User: {session["user_name"]}')
                return {'message': 'label updated'}
            return {'Error': 'Label not present in given note'}

    def delete(self, id):
        req_data = request.data
        body = json.loads(req_data)
        label = body.get('label')

        note = Notes.objects.filter(id=id, user_name=session['user_name']).first()

        list_label = note.label
        for data in list_label:
            print(data.label)
            if data.label == label:
                print(data.label)
                list_label.remove(data)
                note.update(label=list_label)
                custome_logger.logger.info(f'Label is deleted of notes of id:{id} by User: {session["user_name"]}')
                return {'message': 'label removed'}
        return {'Error': 'label not found in this note'}


class GetByLabel(Resource):
    method_decorators = {'get': [auth.login_required]}

    def get(self, label):
        list_notes = []
        note = Notes.objects.filter(user_name=session['user_name'])
        for data in note:
            for lb in data.label:
                if lb.label == label:
                    dict_ = {'id': data.id, 'topic': data.topic, 'desc': data.desc, 'label': [lb.label for lb in data.label]}
                    list_notes.append(dict_)
        return {'data': list_notes}


class Home(Resource):
    # import main
    method_decorators = {'get': [token_required]}

    # @main.cache.memoize(timeout=10)
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
                    dict_itr = {'id': itr.id, 'topic': itr.topic, 'desc': itr.desc, 'color': itr.color, 'label': [lb.label for lb in itr.label]}
                    list_user.append(dict_itr)
                dict_all[data.user_name] = list_user

            return make_response(dict_all)
        data_ = Notes.objects.filter(user_name=user_name)
        for data in data_:
            dict_ = {'id': data.id, 'topic': data.topic, 'desc': data.desc, 'label': [lb.label for lb in data.label]}
            list_notes.append(dict_)

        return make_response(jsonify(list_notes), 200)
