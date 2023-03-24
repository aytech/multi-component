from utilities.errors.BaseError import BaseError


class AuthorisationError(BaseError):

    def __init__(self):
        self.message = 'Authorisation error raised'
