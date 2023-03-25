from datetime import datetime, timedelta


class DateProcessor:
    @staticmethod
    def hours_passed(from_date: str) -> int:
        from_date_date: datetime = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S.%f')
        current_date: datetime = datetime.now()
        delta: timedelta = current_date - from_date_date

        hours: int = delta.days * 24 if delta.days > 0 else 0

        return hours + (delta.seconds // 3600)
