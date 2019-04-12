"""This module contains CRUD methods for the flask API instantiated
at app.py. These methods are designed to work with a running instance
of redis."""

from datetime import datetime
from hashlib import blake2b

from server.redis.redis_local import redis_instance

# TODO: Include subtasks in Hash model
class ToDoUser:
    """
    All ToDo list tasks are centralized in this ToDoUser class.
    """

    def __init__(self, user_obj, r=redis_instance):
        self.r = r
        self.userid = user_obj["id"]
        self.name = user_obj["name"]
        self.mykey = "Todos:users:" + str(self.userid) + ":tasks:"
        self.my_task_ids = self.mykey + "all_task_ids"
        self.r.hmset("Todos:users:" + str(self.userid), user_obj)

    # Create Methods
    def set_task(self, task_obj):
        """
        Establishes key value stores in redis for rapid querying of task_ids for specified
        queries.
        Task_ids are used in subsequent queries for accessing hash map of specific task
        field data
        """
        task_id, task_obj, task_hash_key = self._initialize_redis_task(task_obj)
        self._initialize_redis_hashmap(task_hash_key, task_obj)
        self._set_task(task_id, task_obj)

    # Retrieve Methods

    def get_all_tasks(self):
        """
        Returns a generator object with hash results of all available task_ids.
        """
        tasks = self.r.smembers(self.my_task_ids)
        for item in self._get_tasks(tasks):
            yield item

    def get_one_task(self, title):
        """
        Returns a single task object from a given task title.
        Titles must be unique, regardless of categories.
        """
        task_id = str(_blake2b_hash_title(title))
        task = self.r.hgetall(self.mykey + task_id)
        return task

    def get_category_tasks(self, category):
        """
        Returns a generator object with hash results of task_id keys with given ``category``

        ``category`` should be passed as a string.
        """
        tasks = self.r.smembers(self.mykey + category + "_task_ids")
        for item in self._get_tasks(tasks):
            yield item

    def get_duedate_range(self, start, end):
        """
        Returns a generator object with the hash results of task_id keys with due dates
        between ``start`` and ``end``.

        ``start`` and ``end`` should be passed as datetime objects in python.
        """
        # start, end = map(self._convert_datetime, (start, end))  ### DEPRECATED
        tasks = self.r.zrangebyscore(self.mykey + "due_sort_all_task_ids", start, end)
        for item in self._get_tasks(tasks):
            yield item

    def get_user_id(self):
        """Returns active user_id"""
        return self.userid

    # Delete Methods
    def delete_tasks(self, titles):
        """
        Must give the category along with a potential list of task_ids
        """
        tasks_data = []
        for title in titles:
            tasks_data.append(self._delete_one_task(title))

        for task_id, category in tasks_data:
            hash_key = self.mykey + str(task_id)
            self.r.hdel(hash_key, "*")
            self.r.srem(self.my_task_ids, task_id)
            self.r.srem(self.mykey + str(category) + "_task_ids", task_id)
            self.r.zrem(self.mykey + "due_sort_all_task_ids", task_id)

    # Class Based Helper Function

    def _set_task(self, task_id, task_obj):
        """Stores all task_ids at self.mykey:all_task_ids.

        Stores by category at self.mykey:<category>_task_ids.

        Stores by due_date in ascending order at
        self.mykey:due_sort_all_taks_ids:<task_id>:<int_due_date> if due date is available"""
        self.r.sadd(self.my_task_ids, task_id)
        self.r.sadd(self.mykey + task_obj["category"] + "_task_ids", task_id)
        print(task_obj["due_date"])
        if task_obj["due_date"]:
            self.r.zadd(
                self.mykey + "due_sort_all_task_ids", {task_id: task_obj["due_date"]}
            )

    def _initialize_redis_hashmap(self, task_hash_key, task_obj):
        """Creates a hash_map of field value pairs for a particular user's task stored
        At location self.mykey:<task_id>."""
        self.r.hmset(task_hash_key, task_obj)

    def _initialize_redis_task(self, task_obj):
        """Hashes task title, returns task_id. Also processes dates and compiles
        task_hash_key for redis database"""
        task_id = str(_blake2b_hash_title(task_obj["title"]))

        task_obj["date_created"], task_obj["due_date"] = _convert_dates(task_obj)

        task_hash_key = self.mykey + task_id
        return task_id, task_obj, task_hash_key

    def _get_tasks(self, task_ids):
        task_objs = []
        for task in task_ids:
            task_obj = self.r.hgetall(self.mykey + str(task))
            task_obj.update({"key":task})
            task_objs.append(task_obj)
            yield task_obj


    def _set_sub_tasks(self, task_id, *subtasks):
        print(*subtasks)
        current = self._get_sub_tasks(task_id)
        print(current)
        self.r.rpush(self.mykey + task_id + ":subtasks", *subtasks)

    def _get_sub_tasks(self, task_id):
        subtask_list = self.r.lrange(
            self.mykey + task_id + ":subtasks",
            0,
            self.r.llen(self.mykey + task_id + ":subtasks"),
        )
        return subtask_list

    def _delete_one_task(self, title):
        """
        Deletes a single task given a specific task title.
        """
        task_id = str(_blake2b_hash_title(title))
        category = self.r.hmget(self.mykey + task_id, "category")
        return task_id, category[0]

    # Dunder Methods

    def __repr__(self):
        tot_tasks = self.r.scard(self.my_task_ids)
        if tot_tasks:
            return "User(user_id: %r, name: %r, tasks: %r)" % (
                self.userid,
                self.name,
                tot_tasks,
            )
        return "User(user_id: %r, name: %r, tasks: 0)" % (self.userid, self.name)


# General Helper Functions
def _convert_dates(task_obj):
    """Creates integer value from datetime object, and processes missing values"""
    due_str = task_obj.get("due_date", "")
    print(due_str)

    format_template = "%Y%m%d%H%M%S"
    created_str = task_obj.get(
        "date_created", datetime.strftime(datetime.utcnow(), format_template)
    )
    print(due_str)
    if due_str:
        return int(created_str), int(due_str)
    return int(created_str), ""


def _stringify_datetime(date):
    year, month, day, hour, minute, second = map(
        int, (date[0:4], date[4:6], date[6:8], date[8:10], date[10:12], date[12:14])
    )
    date = datetime(year, month, day, hour, minute, second).strftime(
        "Date: %m-%d-%Y Time: %H:%M:%S"
    )
    return date


def _blake2b_hash_title(string):
    hashed_title = blake2b(digest_size=10)
    title = bytes(string, encoding="utf-8")
    hashed_title.update(title)
    task_id = hashed_title.hexdigest()
    return task_id
