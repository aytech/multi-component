from utilities.errors.BaseError import BaseError


class TimeoutReceivedError(BaseError):
    def __init__(self, reason: str):
        self.message = 'Timeout error raised, reason: %s' % reason
