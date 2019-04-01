from datetime import datetime
from types import GeneratorType

from pytest import raises, mark
from fakeredis import FakeStrictRedis


from server.redis.redis_methods import (
    ToDoUser,
    _blake2b_hash_title,
    _convert_dates,
    _initialize_redis_hashmap,
    _stringify_datetime,
)


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
        "date_created": "201901201518",
        "due_date": "201901201519",
    },
    {
        "title": "Play Saxophone",
        "category": "Practice",
        "date_created": "201804201934",
        "due_date": "201901201520",
    },
    {
        "title": "Grocery Shop",
        "category": "chores",
        "date_created": "201901201521",
        "due_date": "",
    },
    {
        "title": "Play Clarinet",
        "category": "Practice",
        "date_created": "201901201523",
        "due_date": "201901201524",
    },
]


user = ToDoUser(user_obj, r)

for i, task in enumerate(task_objs):
    user.set_task(task_objs[i])


class TestToDoUser:
    def test_get_all_tasks(self):
        x = user.get_all_tasks()
        assert isinstance(x, GeneratorType) == True
        assert isinstance(next(x), object) == True

    def test_get_one_task(self):
        actual = user.get_one_task("Grocery Shop")
        assert actual == {
            "title": "Grocery Shop",
            "category": "chores",
            "date_created": "201901201521",
            "due_date": "",
        }

    def test_get_category_tasks(self):
        x = user.get_category_tasks("Practice")
        assert isinstance(x, GeneratorType) == True
        assert isinstance(next(x), object) == True

    def test_get_date_range(self):
        x = user.get_date_range(201901201518, 201901201524)
        assert isinstance(x, GeneratorType) == True
        assert isinstance(next(x), object) == True
        # Check the items in the generator
        assert sum(1 for i in x) == 2

    def test_get_user_id(self):
        assert user.get_user_id() == "230872340987520234985"

    def test__repr__(self):
        assert ToDoUser(user_obj, r).__repr__() == (
            "User(user_id: '230872340987520234985', name: 'Brian Fredericks', tasks: 4)"
        )

    def test__delete_one_task(self):
        actual = user._delete_one_task("Grocery Shop")
        assert actual == ("fb4b0dc2756d5131a6f5", "chores")

    def test_delete_tasks(self):
        user.delete_tasks(["Grocery Shop"])
        assert sum(1 for i in user.get_all_tasks()) == 3

    # @mark.parametrize("task_obj_input,expected", {(task_objs[0], 0)})
    def test__initialize_redis_task(self):
        assert user._initialize_redis_task(task_objs[0]) == (
            "0480a119a478b410bba4",
            {
                "title": "Do your laundry",
                "category": "chores",
                "date_created": 201901201518,
                "due_date": 201901201519,
            },
            "Todos:users:230872340987520234985:tasks:0480a119a478b410bba4",
        )

    def test__get_tasks(self):
        x = user._get_tasks([0, 1, 2, 3])
        assert isinstance(x, GeneratorType) == True
        assert next(x) == {}

    @mark.parametrize(
        "hash_input,expected",
        {
            ("check this out", "f7d32a9739d22c399cc0"),
            ("1-0918234-34-098235098723-#$)(*@&#$%)(*&!#%_(*", "2c9af44e7aab5c9c7a20"),
        },
    )
    def test__hash(self, hash_input, expected):
        assert _blake2b_hash_title(hash_input) == expected

    def test__convert_dates(self):
        assert _convert_dates(task_objs[3]) == (201901201523, 201901201524)
        assert _convert_dates(task_objs[2]) == (201901201521, "")

    @mark.parametrize(
        "intdate_input,expected",
        {("20190330185242", "Date: 03-30-2019 Time: 18:52:42")},
    )
    def test__stringify_datetime(self, intdate_input, expected):
        assert _stringify_datetime(intdate_input) == expected

