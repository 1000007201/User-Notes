from .models import Label


def valid_add_label(body):
    label = body.get('label')
    user_id = body.get('user_id')
    lb = Label.objects.filter(user_id=user_id, label=label).first()
    if lb:
        return {'Error': 'Label already exist', 'code': 409}


def valid_delete_label(label):
    lb = Label.objects.filter(label=label).first()
    if not lb:
        return {'Error': 'Label not Exist', 'code': 409}
