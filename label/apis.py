from flask_restful import Resource
from flask import request, json, session
from middleware import auth
from .validators import valid_add_label, valid_delete_label
from .models import Label


class AddLabel(Resource):
    method_decorators = {'post': [auth.login_required]}

    def post(self):
        """
            This API is used to create a label
            @param request: label name
            @return: Creates label
        """
        req_data = request.data
        body = json.loads(req_data)
        body['user_id'] = session['user_id']
        valid_data = valid_add_label(body)
        if valid_data:
            return {'data': valid_data, 'code': 500}
        lb = Label(**body)
        lb.save()
        return {'message': 'label added', 'code': 200}


class DeleteLabel(Resource):
    method_decorators = {'delete': [auth.login_required]}

    def delete(self, label):
        """
            This API is used to delete existing label
            @param label_id: primary_key of the specific label
            @return: delete the label
        """
        valid_data = valid_delete_label(label)
        user_id = session['user_id']
        if valid_data:
            return valid_data
        lb = Label.objects.filter(user_id=user_id, label=label).first()
        lb.delete()
        return {'message': 'label deleted', 'code': 200}
