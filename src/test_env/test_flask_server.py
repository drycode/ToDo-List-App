from datetime import datetime
from types import GeneratorType

from server.redis.redis_methods import ToDoUser
from pytest import raises, mark
from fakeredis import FakeStrictRedis

r = FakeStrictRedis()


user_obj = {
    "email": "testytest@gmail.com",
    "family_name": "Fredericks",
    "given_name": "Brian",
    "id": "230872340987520234985",
    "link": "https://plus.google.com/230872340987520234985",
    "locale": "en",
    "name": "Brian Fredericks",
    "picture": "https://lh3.googleusercontent.com/photo.jpg",
    "verified_email": "true",
}

task_objs = [
    {
        "title": "Do your laundry",
        "category": "chores",
        "date_created": "datetime(2019, 2, 9, 22, 24, 11,346910)",
        "due_date": "datetime(2019, 2, 9, 22, 24, 11,346910)",
    },
    {
        "title": "Play Saxophone",
        "category": "Practice",
        "date_created": "2-3-19",
        "due_date": "datetime(2019, 2, 9, 22, 24, 11,346911)",
    },
    {
        "title": "Grocery Shop",
        "category": "chores",
        "date_created": "2-3-19",
        "due_date": "datetime(2019, 2, 9, 22, 24, 11, 346912)",
    },
    {
        "title": "Play Clarinet",
        "category": "Practice",
        "date_created": "2-3-19",
        "due_date": "None",
    },
]

for i, task in enumerate(task_objs):
    r.hmset(i, task)

user = ToDoUser(user_obj)


class TestToDoUser:
    # @mark.parametrize("task_obj_input,expected", {(task_objs[0], 0)})
    def test__initialize_redis_task(self):
        assert user._initialize_redis_task(task_objs[0]) == (
            "0480a119a478b410bba4",
            {
                "category": "chores",
                "date_created": 20190209222411,
                "due_date": 20190209222411,
                "title": "Do your laundry",
            },
            "Todos:users:230872340987520234985:tasks:0480a119a478b410bba4",
            True,
        )

    def test__get_tasks(self):
        x = user._get_tasks([0, 1, 2, 3])
        assert isinstance(x, GeneratorType) == True

    @mark.parametrize(
        "hash_input,expected",
        {
            ("check this out", "f7d32a9739d22c399cc0"),
            ("1-0918234-34-098235098723-#$)(*@&#$%)(*&!#%_(*", "2c9af44e7aab5c9c7a20"),
        },
    )
    def test__hash(self, hash_input, expected):
        assert user._blake2b_hash_title(hash_input) == expected

    @mark.parametrize(
        "datetime_input,expected",
        {(datetime(2019, 3, 30, 18, 52, 42, 90443), 20190330185242)},
    )
    def test__convert_datetime(self, datetime_input, expected):
        assert user._convert_datetime(datetime_input) == expected

    @mark.parametrize(
        "intdate_input,expected",
        {("20190330185242", "Date: 03-30-2019 Time: 18:52:42")},
    )
    def test__stringify_datetime(self, intdate_input, expected):
        assert user._stringify_datetime(intdate_input) == expected
