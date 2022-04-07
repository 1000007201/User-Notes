

class CustomException(Exception):
    def __init__(self, msg, code):
        self.Error = msg
        self.code = code


class NotFoundException(CustomException):
    pass


class AlreadyExistException(CustomException):
    pass


class NullValueException(CustomException):
    pass


class InternalServer(CustomException):
    pass
