import re
import unittest

from db.dao import UserDao
from utilities.DateProcessor import DateProcessor


class TestUserDao(unittest.TestCase):
    def test_minimal_dao(self):
        dao: UserDao = UserDao(bio='', distance_mi=1, liked=False, name='Oleg', s_number=1, user_id='1')
        expected_str: str = '''
            User(age=0, bio=, birth_date=, city=, created=%s, distance=1.6, liked=False, name=Oleg, photos=[], 
            s_number=1, user_id=1)
        ''' % DateProcessor.get_current_date()
        expected_str = re.sub(r'\s+', ' ', expected_str)
        self.assertEqual(expected_str.strip(), str(dao))
