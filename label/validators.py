from .models import Label
from common.custom_exceptions import AlreadyExistException, NotFoundException


def valid_add_label(body):
    label = body.get('label')
    user_id = body.get('user_id')
    try:
        lb = Label.objects.filter(user_id=user_id, label=label).first()
        if lb:
            raise AlreadyExistException('Label already exist', 409)
    except AlreadyExistException as exception:
        return exception.__dict__
    except Exception as e:
        return {'Error': str(e), 'code': 500}


def valid_delete_label(label):
    try:
        lb = Label.objects.filter(label=label).first()
        if not lb:
            raise NotFoundException('Label not Exist', 409)
    except NotFoundException as exception:
        return exception.__dict__
    except Exception as e:
        return {'Error': str(e), 'code': 500}
