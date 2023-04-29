import datetime
import json
import unittest

from db.dao import UserDao
from utilities.Results import Results
from utilities.errors.GenericError import GenericError
from utilities.errors.TimeoutReceivedError import TimeoutReceivedError


class TestResults(unittest.TestCase):
    def test_input_errors(self):
        with self.assertRaises(GenericError, msg='Response data is null'):
            Results.user_list()
        with self.assertRaises(GenericError, msg='Response data is null'):
            Results.user_list(json.loads('{}'))
        with self.assertRaises(TimeoutReceivedError, msg=''):
            Results.user_list(json.loads('{"data": {"timeout": 1}}'))

    def test_empty_results(self):
        empty_data: str = json.loads('{"data": {}}')
        self.assertEqual([], Results.user_list(empty_data))
        empty_result: str = json.loads('{"data": {"results": [{}]}}')
        self.assertEqual([], Results.user_list(empty_result))
        wrong_type: str = json.loads('{"data": {"results": [{"type": "foo"}]}}')
        self.assertEqual([], Results.user_list(wrong_type))

    def test_user_parsing(self):
        birth_date: str = '1981-05-02T07:19:10.969Z'
        payload: str = json.loads('''
            {
                "data": {
                    "results": [
                        {
                            "distance_mi": 2,
                            "s_number": 1,
                            "type": "user",
                            "user": {
                                "_id": "123",
                                "bio": "Some bio",
                                "birth_date": "%s",
                                "city": {
                                    "name": "Prague"
                                },
                                "name": "Oleg",
                                "photos": [
                                    {
                                        "id": "1",
                                        "url": "http://photo.id.1"
                                    },
                                    {
                                        "id": "2",
                                        "url": "http://photo.id.2"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ''' % birth_date)
        users: list[UserDao] = Results.user_list(payload)
        for user in users:
            self.assertEqual(user.age, 42)
            self.assertEqual(user.bio, 'Some bio')
            self.assertEqual(user.birth_date, '2 May, 1981')
            self.assertEqual(user.city, 'Prague')
            self.assertEqual(user.created, datetime.datetime.now().strftime('%Y-%b-%d %H:%M:%S'))
            self.assertEqual(user.distance, 3.2)
            self.assertEqual(user.liked, False)
            self.assertEqual(user.name, 'Oleg')
            self.assertEqual(len(user.photos), 2)
            self.assertEqual(user.photos[0].created, datetime.datetime.now().strftime('%Y-%b-%d %H:%M:%S'))
            self.assertEqual(user.photos[0].photo_id, '1')
            self.assertEqual(user.photos[0].url, 'http://photo.id.1')
            self.assertEqual(user.photos[1].created, datetime.datetime.now().strftime('%Y-%b-%d %H:%M:%S'))
            self.assertEqual(user.photos[1].photo_id, '2')
            self.assertEqual(user.photos[1].url, 'http://photo.id.2')
            self.assertEqual(user.s_number, 1)
            self.assertEqual(user.user_id, '123')
