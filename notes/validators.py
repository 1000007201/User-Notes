
color_choices = ('red', 'green', 'blue', 'black')


def validate_add_notes(body):
    topic = body.get('topic')
    desc = body.get('desc')
    if not desc or not topic:
        return {'Error': 'You have to fill both parameters'}
    if body.get('color'):
        if body.get('color') not in color_choices:
            return {'Error': 'Given color is not valid'}


def validate_add_label(body):
    label = body.get('label')
    if not label:
        return {'Error': 'Label can not be null'}
