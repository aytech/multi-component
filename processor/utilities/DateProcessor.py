import calendar
from datetime import datetime, timedelta


class DateProcessor:
    @staticmethod
    def hours_passed(from_date: str) -> int:
        from_date_date: datetime = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S.%f')
        current_date: datetime = datetime.now()
        delta: timedelta = current_date - from_date_date

        hours: int = delta.days * 24 if delta.days > 0 else 0

        return hours + (delta.seconds // 3600)

    @staticmethod
    def get_current_date() -> str:
        dt: datetime = datetime.now()
        return dt.strftime('%Y-%b-%d %H:%M:%S')

    @staticmethod
    def get_converted_birth_date(birth_date: str) -> datetime:
        return datetime.strptime(birth_date, '%Y-%m-%dT%H:%M:%S.%fZ')

    @staticmethod
    def get_user_birth_date(birth_date: str) -> str:
        date = DateProcessor.get_converted_birth_date(birth_date=birth_date)
        return '%s %s, %s' % (date.day, calendar.month_name[date.month], date.year)

    @staticmethod
    def get_user_age(birth_date: str) -> int:
        birth_date: datetime = DateProcessor.get_converted_birth_date(birth_date=birth_date)
        return int((datetime.now() - birth_date).days / 365)
