from flask_restful import Resource
from flask import request, session, json
from .validators import validate_add_notes, validate_add_label
from .utils import token_required
from .models import Notes
from label import models as md
from user import models
from middleware import auth
from common.custome_logger import logger
from common.utils import get_cache, do_cache
from common.custom_exceptions import NotFoundException, AlreadyExistException


class AddNote(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        req_data = request.data
        body = json.loads(req_data)
        # image_ = request.files['image']
        try:
            body['user_id'] = session['user_id']
            user = models.Users.objects.filter(id=session['user_id']).first()
            body['user_name'] = user.user_name
            label_ = body['label']
            del body['label']
            validated_data = validate_add_notes(body)
            if validated_data:
                return {'data': validated_data, 'code': 409}
            notes = Notes(**body)
            # notes.image.replace(image_, filename='my_image')
            notes.save()
            # label = body.get('label')
            if label_:
                lb = md.Label.objects.filter(user_id=session['user_id'], label=label_).first()
                if not lb:
                    lb = md.Label(user_id=session['user_id'], label=label_)
                    lb.save()
                notes.update(push__label=lb)
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        logger.info(f'Notes added by User: {notes.user_name}')
        return {'message': 'Notes Added', 'code': 200}


class NotesOperation(Resource):
    method_decorators = {'patch': [auth.login_required], 'delete': [auth.login_required]}

    def patch(self, note_id):
        try:
            note = Notes.objects.filter(id=note_id, user_id=session['user_id']).first()
            desc = request.form.get('Description')
            note.update(desc=desc)
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        logger.info(f'Notes are updated of id:{note_id} by User_id: {session["user_id"]}')
        return {'message': 'Notes updated', 'code': 200}

    def delete(self, note_id):
        try:
            note = Notes.objects.filter(id=note_id,  user_id=session['user_id']).first()
            if not note.is_trash:
                raise NotFoundException('Note not found in trash', 404)
            if note.is_trash:
                note.delete()
            logger.info(f'Notes are deleted of id:{note_id} by User_id: {session["user_id"]}')
            return {'message': 'Notes Deleted', 'code': 200}
        except NotFoundException as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'code': 500}


class NoteLabel(Resource):
    method_decorators = {'post': [auth.login_required], 'patch': [auth.login_required], 'delete': [auth.login_required]}

    def post(self, note_id):
        req_data = request.data
        body = json.loads(req_data)
        validate_data = validate_add_label(body)
        if validate_data:
            return {'data': validate_data, 'code': 404}
        label = body.get('label')
        user_id = session['user_id']
        try:
            label_data = md.Label.objects.filter(user_id=user_id, label=label).first()
            if not label_data:
                label_data = md.Label(user_id=user_id, label=label)
                label_data.save()
            note = Notes.objects.filter(user_id=session['user_id'], id=note_id).first()
            if not note:
                raise NotFoundException('Note is not present', 404)
                # return {'Error': 'Note is not present', 'code': 404}
            for data in note.label:
                if data.label == label:
                    raise AlreadyExistException('label already present in this note', 404)
                    # return {'Error': 'label already present in this note', 'code': 404}
            note.update(push__label=label_data)
        except NotFoundException as exception:
            return exception.__dict__
        except AlreadyExistException as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        logger.info(f'Label is added to notes of id:{note_id} by User_id: {session["user_id"]}')
        return {'message': 'label added', 'code': 200}

    def patch(self, note_id):
        req_data = request.data
        body = json.loads(req_data)
        old_label = body.get('label')
        new_label = body.get('new_label')
        user_id = session['user_id']
        note = Notes.objects.filter(id=note_id, user_id=user_id).first()
        label2 = md.Label.objects.filter(user_id=user_id, label=new_label).first()
        if not label2:
            label2 = md.Label(user_id=user_id, label=new_label)
            label2.save()
        label_list = note.label
        for i in label_list:
            if i.label == old_label:
                label_list.remove(i)
                label_list.append(label2)
                note.update(label=label_list)
                logger.info(f'Label is updated of notes of id:{note_id} by User_id: {session["user_id"]}')
                return {'message': 'label updated', 'code': 200}
        return {'Error': 'Label not present in given note', 'code': 404}

    def delete(self, note_id):
        req_data = request.data
        body = json.loads(req_data)
        label = body.get('label')

        note = Notes.objects.filter(id=note_id, user_id=session['user_id']).first()

        list_label = note.label
        for data in list_label:
            print(data.label)
            if data.label == label:
                print(data.label)
                list_label.remove(data)
                note.update(label=list_label)
                logger.info(f'Label is deleted of notes of id:{note_id} by User_id: {session["user_id"]}')
                return {'message': 'label removed', 'code': 200}
        return {'Error': 'label not found in this note', 'code': 404}


class GetByLabel(Resource):
    method_decorators = {'get': [auth.login_required]}

    def get(self, label):
        user_id = session['user_id']
        key = f'getbylabel_{user_id}'
        value = get_cache(key)
        if value:
            print('red')
            data_ = json.loads(value)
            return {'data': data_, 'code': 200}
        list_notes = []
        note = Notes.objects.filter(user_id=user_id, is_trash=False)
        for data in note:
            for lb in data.label:
                if lb.label == label:
                    dict_ = {'id': data.id, 'user_id': data.user_id, 'topic': data.topic, 'desc': data.desc, 'label': [lb.label for lb in data.label]}
                    list_notes.append(dict_)
        do_cache(key, list_notes, 30)
        print('data')
        return {'data': list_notes, 'code': 200}


class Home(Resource):
    method_decorators = {'get': [token_required]}

    def get(self, user_id):
        key = f'home_{user_id}'
        value = get_cache(key)
        if value:
            print("from redis")
            _data = json.loads(value)
            return {'data': _data}
        list_notes = []
        data_ = models.Users.objects.filter(id=user_id).first()
        if data_.is_super_user:
            dict_all = {}
            data_user = models.Users.objects()
            for data in data_user:
                note = Notes.objects.filter(user_id=data.id, is_trash=False, is_pinned=True)
                list_user = []
                for itr in note:
                    dict_itr = {'id': itr.id, 'user_id': itr.user_id, 'topic': itr.topic, 'desc': itr.desc, 'color': itr.color, 'label': [lb.label for lb in itr.label]}
                    list_user.append(dict_itr)
                note = Notes.objects.filter(user_id=data.id, is_trash=False, is_pinned=False)
                for itr in note:
                    dict_itr = {'id': itr.id, 'user_id': itr.user_id, 'topic': itr.topic, 'desc': itr.desc, 'color': itr.color, 'label': [lb.label for lb in itr.label]}
                    list_user.append(dict_itr)
                dict_all[data.user_name] = list_user
            key = f'home_{user_id}'
            do_cache(key, dict_all, 30)
            # print("from data")
            return {'data': dict_all, 'code': 200}
        data_ = Notes.objects.filter(user_id=user_id, is_trash=False, is_pinned=True)
        for data in data_:
            dict_ = {'id': data.id, 'user_id': data.user_id, 'topic': data.topic, 'desc': data.desc, 'label': [lb.label for lb in data.label]}
            list_notes.append(dict_)
        data_ = Notes.objects.filter(user_id=user_id, is_trash=False, is_pinned=False)
        for data in data_:
            dict_ = {'id': data.id, 'user_id': data.user_id, 'topic': data.topic, 'desc': data.desc, 'label': [lb.label for lb in data.label]}
            list_notes.append(dict_)
        key = f'home_{user_id}'
        do_cache(key, list_notes, 30)
        # print("from data")

        return {'data': list_notes, 'code': 200}


class PinNote(Resource):
    method_decorators = {'patch': [auth.login_required]}

    def patch(self, note_id):
        try:
            note = Notes.objects.filter(id=note_id, user_id=session['user_id'])
            if not note:
                raise NotFoundException('Note not found', 404)
            note.update(is_pinned=True)
        except NotFoundException as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': 'Note is pinned', 'code': 200}


class UnpinNote(Resource):
    method_decorators = {'patch': [auth.login_required]}

    def patch(self, note_id):
        try:
            note = Notes.objects.filter(id=note_id, user_id=session['user_id'])
            if not note:
                raise NotFoundException('Note not found', 404)
            note.update(is_pinned=False)
        except NotFoundException as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': 'Note is Unpinned', 'code': 200}


class NoteAddTrash(Resource):
    method_decorators = {'patch': [auth.login_required]}

    def patch(self, note_id):
        try:
            note = Notes.objects.filter(id=note_id, user_id=session['user_id'])
            if not note:
                raise NotFoundException('Note not found', 404)
            note.update(is_trash=True)
        except NotFoundException as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': 'Note is moved to trash', 'code': 200}


class NoteRemoveTrash(Resource):
    method_decorators = {'patch': [auth.login_required]}

    def patch(self, note_id):
        try:
            note = Notes.objects.filter(id=note_id, user_id=session['user_id'])
            if not note:
                raise NotFoundException('Note not found', 404)
            note.update(is_trash=False)
        except NotFoundException as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': 'Note is removed from trash', 'code': 200}
