import unittest
from server.redis_methods import *
from datetime import datetime


# TODO: read about mocking redis, integration testing
# https://pypi.org/project/fakeredis/
# Read about dependency injection
dan = ToDoUser(user_obj)

class RedisTestCase(unittest.TestCase):
    def test_blake2b_hash_title(self):
        self.assertEqual(dan._blake2b_hash_title("banana"), '2075c624a8a0c8a07d95')
    
    def test_blake2b_hash_number(self):
        self.assertEqual(dan._blake2b_hash_title('11111111'), '7e21eef647d0d58514d0')

    def test_blake2b_hash_long_specials(self):
        self.assertEqual(dan._blake2b_hash_title("!@#$%^&*)(_+:?><}{|][\]\)"), "3844ebe5de1d5e3cef45")

    def test_convert_datetime(self):
        self.assertEqual(dan._convert_datetime(datetime(2018, 3, 21, 21, 4, 34)), 20180321210434)
    
    def test_convert_datetime_string(self):
        self.assertEqual(dan._convert_datetime(eval("datetime(2018, 3, 21, 21, 4, 34)")), 20180321210434)
    
    def test_stringify_datetime(self):
        self.assertEqual(dan._stringify_datetime("20180321210434"), 'Date: 03-21-2018 Time: 21:04:34')

    # def test_get_tasks(self):
    #     self.assertAlmostEqual(dan.get_all_tasks(), "asd")

class ServerTestCase(unittest.TestCase):
    def test_test(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()