import datetime


class RemainingLikesDao:
    likes_remaining: int
    rate_limited_until: datetime

    def __init__(self, likes_remaining: int, rate_limited_until: int = None):
        self.likes_remaining = likes_remaining
        if rate_limited_until is None:
            self.rate_limited_until = datetime.datetime.now()
        else:
            # convert to seconds from millis
            seconds = rate_limited_until // 1000
            local_datetime: datetime = datetime.datetime.utcfromtimestamp(seconds) + datetime.timedelta(hours=2)
            self.rate_limited_until = local_datetime.strftime('%d %B %Y, %H:%M')

    def to_dict(self):
        return {'likes_remaining': self.likes_remaining, 'rate_limited_until': self.rate_limited_until}
