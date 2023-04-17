from utilities.errors.BaseError import BaseError


class AuthorizationError(BaseError):

    def __init__(self):
        self.message = 'Authorization error raised'
