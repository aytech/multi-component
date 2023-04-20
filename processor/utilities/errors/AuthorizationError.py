from utilities.errors.BaseError import BaseError


class AuthorizationError(BaseError):

    def __init__(self, message: str):
        self.message = 'Authorization error raised %s' % message
