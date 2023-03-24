from utilities.errors.BaseError import BaseError


class GenericError(BaseError):

    def __init__(self, reason: str):
        self.message = 'Generic error raised, reason: %s' % reason
