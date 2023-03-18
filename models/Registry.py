from datetime import datetime


class Registry:
    records: dict[str, str]
    log_file_name: str

    def add_user(self, user_id, user_name):
        self.records[user_id] = user_name

    def user_exists(self, user_id):
        return user_id in self.records

    def add_message(self, message: str):
        print(message)
        with open(self.log_file_name, 'a') as file:
            print(message, file=file)

    def flush(self):
        with open(self.log_file_name, 'a') as file:
            print('Total of %s records processed' % len(self.records), file=file)

    def __init__(self):
        self.records = {}
        self.log_file_name = '%s.log' % datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
