"""This module contains CRUD methods for the flask API instantiated
at app.py. These methods are designed to work with a running instance
of redis."""

from datetime import datetime
from hashlib import blake2b

from server.redis.redis_local import r

# TODO: Include subtasks in Hash model
class ToDoUser:
    """
    All ToDo list tasks are centralized in this ToDoUser class.
    """

    def __init__(self, user_obj, r=r):
        self.userid = user_obj["id"]
        self.name = user_obj["name"]
        self.mykey = "Todos:users:" + str(self.userid) + ":tasks:"
        self.my_task_ids = self.mykey + "all_task_ids"
        r.hmset("Todos:users:" + str(self.userid), user_obj)

    # Create Methods
    def set_task(self, task_obj):
        """
        Establishes key value stores in redis for rapid querying of task_ids for specified
        queries.
        Task_ids are used in subsequent queries for accessing hash map of specific task
        field data
        """
        task_id, task_obj, task_hash_key = self._initialize_redis_task(task_obj)
        _initialize_redis_hashmap(task_hash_key, task_obj)
        self._set_task(task_id, task_obj)

    # Retrieve Methods

    def get_all_tasks(self):
        """
        Returns a generator object with hash results of all available task_ids.
        """
        tasks = r.smembers(self.my_task_ids)
        for item in self._get_tasks(tasks):
            yield item

    def get_one_task(self, title):
        """
        Returns a single task object from a given task title.
        Titles must be unique, regardless of categories.
        """
        task_id = _blake2b_hash_title(title)
        task = r.hgetall(self.mykey + task_id)
        return task

    def get_category_tasks(self, category):
        """
        Returns a generator object with hash results of task_id keys with given ``category``

        ``category`` should be passed as a string.
        """
        tasks = r.smembers(self.mykey + category + "_task_ids")
        for item in self._get_tasks(tasks):
            yield item

    def get_duedate_range(self, start, end):
        """
        Returns a generator object with the hash results of task_id keys with due dates
        between ``start`` and ``end``.

        ``start`` and ``end`` should be passed as datetime objects in python.
        """
        # start, end = map(self._convert_datetime, (start, end))  ### DEPRECATED
        tasks = r.zrangebyscore(self.mykey + "due_sort_all_task_ids", start, end)
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
            r.hdel(hash_key, "*")
            r.srem(self.my_task_ids, task_id)
            r.srem(self.mykey + category + "_task_ids", task_id)
            r.zrem(self.mykey + "due_sort_all_task_ids", task_id)

    # Class Based Helper Function

    def _set_task(self, task_id, task_obj):
        """Stores all task_ids at self.mykey:all_task_ids.

        Stores by category at self.mykey:<category>_task_ids.

        Stores by due_date in ascending order at
        self.mykey:due_sort_all_taks_ids:<task_id>:<int_due_date> if due date is available"""
        r.sadd(self.my_task_ids, task_id)
        r.sadd(self.mykey + task_obj["category"] + "_task_ids", task_id)
        print(task_obj["due_date"])
        if task_obj["due_date"]:
            r.zadd(
                self.mykey + "due_sort_all_task_ids", {task_id: task_obj["due_date"]}
            )

    def _initialize_redis_task(self, task_obj):
        """Hashes task title, returns task_id. Also processes dates and compiles
        task_hash_key for redis database"""
        task_id = _blake2b_hash_title(task_obj["title"])

        task_obj["date_created"], task_obj["due_date"] = _convert_dates(task_obj)

        task_hash_key = self.mykey + str(task_id)
        return task_id, task_obj, task_hash_key

    def _get_tasks(self, task_ids):
        return (r.hgetall(self.mykey + str(task)) for task in task_ids)

    def _set_sub_tasks(self, task_id, subtasks=[]):
        r.rpush(self.mykey + task_id, subtasks)

    def _get_sub_tasks(self, task_id):
        subtask_list = r.lrange(self.mykey + task_id, 0, r.llen(self.mykey + task_id))
        return subtask_list

    def _delete_one_task(self, title):
        """
        Deletes a single task given a specific task title.
        """
        task_id = _blake2b_hash_title(title)
        category = r.hmget(self.mykey + str(task_id), "category")
        return task_id, category[0]

    # Dunder Methods

    def __repr__(self):
        try:
            tot_tasks = r.scard(self.my_task_ids)
        except AttributeError:
            tot_tasks = None
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


def _initialize_redis_hashmap(task_hash_key, task_obj):
    """Creates a hash_map of field value pairs for a particular user's task stored
    At location self.mykey:<task_id>."""
    try:
        r.hmset(task_hash_key, task_obj)
    except TypeError:
        print(f"Error in hash_map processing of task {task_obj}")


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
