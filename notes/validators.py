from common.custom_exceptions import NullValueException, NotFoundException
color_choices = ('red', 'green', 'blue', 'black')


def validate_add_notes(body):
    try:
        topic = body.get('topic')
        desc = body.get('desc')
        if not desc or not topic:
            raise NullValueException('You have to fill both parameters', 409)
        if body.get('color'):
            if body.get('color') not in color_choices:
                raise NotFoundException('Given color is not valid', 404)
    except NullValueException as exception:
        return exception.__dict__
    except NotFoundException as exception:
        return exception.__dict__
    except Exception as e:
        return {'Error': str(e), 'code': 500}


def validate_add_label(body):
    try:
        label = body.get('label')
        if not label:
            raise NullValueException('Label can not be null', 409)
    except NullValueException as exception:
        return exception.__dict__
    except Exception as e:
        return {'Error': str(e), 'code': 500}
