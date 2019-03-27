from datetime import datetime
from hashlib import blake2b

from redis_local import r

# TODO: Include subtasks in Hash model
class ToDoUser:
    def __init__(self, user_obj):
        self.userid = user_obj["id"]
        self.name = user_obj["name"]
        self.mykey = "Todos:users:" + str(self.userid) + ":tasks:"
        self.my_task_ids = self.mykey + "all_task_ids"
        r.hmset("Todos:users:" + str(self.userid), user_obj)

    """"All Create/Update functions will begin here and will continue through
    to the next explicit comment."""
    # Sets up all parts of the hash map

    # TODO: Refactor to put set methods into helper functions
    # TODO: Redis transactions?...
    def set_task(self, task_obj):
        """
        Establishes key value stores in redis for rapid querying of task_ids for specified
        queries. 

        Task_ids are used in subsequent queries for accessing hash map of specific task
        field data, 
        """
        task_id, task_obj, task_hash_key, due_date = self._initialize_redis_task(task_obj)
        self._initialize_redis_hashmap(task_hash_key, task_obj)

        

        # Stores all of the user's task_id keys
        # At location self.mykey:all_task_ids
        r.sadd(self.my_task_ids, task_id)

        # Stores user's task_ids for a particular category
        # At location self.mykey:<category>_task_ids
        r.sadd(self.mykey + task_obj["category"] + "_task_ids", task_id)

        # Stores user's task_ids with due_date sorted by ascending order
        # print(task_obj['due_date'])
        if due_date:
            r.zadd(
                self.mykey + "due_sort_all_task_ids", {task_id: task_obj["due_date"]}
            )

    """All Retrieval functions will begin here and will continue through to the next
    explicit comment."""

    # Queries all tasks
    def get_all_tasks(self):
        """
        Returns a generator object with hash results of all available task_ids.
        """
        tasks = r.smembers(self.my_task_ids)
        for item in self._get_tasks(tasks):
            yield item
        
    def get_one_task(self, title):
        task_id = self._blake2b_hash_title(title)
        task = r.hgetall(self.mykey + task_id)
        return task

    # Queries tasks by category
    def get_category_tasks(self, category):
        """
        Returns a generator object with hash results of task_id keys with given ``category``

        ``category`` should be passed as a string.
        """
        tasks = r.smembers(self.mykey + category + "_task_ids")
        for item in self._get_tasks(tasks):
            yield item

    # Queries specific date range
    def get_date_range(self, start, end):
        """
        Returns a generator object withthe hash results of task_id keys with due dates 
        between ``start`` and ``end``. 

        ``start`` and ``end`` should be passed as datetime objects in python.
        """
        start, end = map(self._convert_datetime, (start, end))
        tasks = r.zrangebyscore(self.mykey + "due_sort_all_task_ids", start, end)
        for item in self._get_tasks(tasks):
            yield item

    def delete_tasks_by_category(self, category, task_ids):
        """
        Must give the category along with a potential list of task_ids
        """
        print(task_ids)
        print(category)
        keys = [self.mykey + str(task_ids) for key in task_ids]
        for key in keys:
            r.delete(key)
        for task in task_ids:
            task = self._blake2b_hash_title(task)
            r.srem(self.my_task_ids, task)
            r.srem(self.mykey + category + "_task_ids", task)
            r.zrem(self.mykey + "due_sort_all_task_ids", task)

    def delete_one_task(self, title):
        task_id = self._blake2b_hash_title(title)
        category = r.hget(self.mykey + task_id, "category")
        self.delete_tasks_by_category(category, task_id)

    def get_user_id(self):
        return self.userid

    """Class based helper functions will begin here and will continue through to the next
    explicit comment."""
    def _initialize_redis_task(self, task_obj):
        task_id = self._blake2b_hash_title(task_obj["title"])

        # TODO: use get() method from defaultdict
        # https://www.programiz.com/python-programming/methods/dictionary/get
        # Converts datetime object to integer value for sorting
        # task_obj['date_created'] = self._convert_datetime(task_obj.get('date_created', datetime.utcnow()))
        if not task_obj["date_created"]:
            task_obj["date_created"] = self._convert_datetime(datetime.utcnow())
        else:
            task_obj["date_created"] = self._convert_datetime(
                eval(task_obj["date_created"])
            )

        try:
            task_obj["due_date"] = self._convert_datetime(eval(task_obj["due_date"]))
            print(task_obj["due_date"])
            due_date = True
        except AttributeError:
            task_obj["due_date"] = str(None)
            due_date = False

        task_hash_key = self.mykey + str(task_id)
        return task_id, task_obj, task_hash_key, due_date

    def _initialize_redis_hashmap(self, task_hash_key, task_obj):
        # Creates a hash_map of field value pairs for a particular user's task stored
        # At location self.mykey:<task_id>.
        # This hash will be queried for task data specific to a specific task_id
        try:
            r.hmset(task_hash_key, task_obj)
        except:
            print("Error in hash_map processing of task {task_obj}")

    # Creates integer value of datetime
    def _convert_datetime(self, date):
        date = date.strftime("%Y%m%d%H%M%S")
        return int(date)

    def _stringify_datetime(self, date):
        year, month, day, hour, minute, second = map(
            int, (date[0:4], date[4:6], date[6:8], date[8:10], date[10:12], date[12:14])
        )
        date = datetime(year, month, day, hour, minute, second).strftime(
            "Date: %m-%d-%Y Time: %H:%M:%S"
        )
        return date

    def _get_tasks(self, tasks):
        return (r.hgetall(self.mykey + task) for task in tasks)

    def _blake2b_hash_title(self, string):
        h = blake2b(digest_size=10)
        title = bytes(string, encoding="utf-8")
        h.update(title)
        task_id = h.hexdigest()
        return task_id

    """Dunder methods stored here."""

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
        else:
            return "User(user_id: %r, name: %r, tasks: 0)" % (self.userid, self.name)

    def set_sub_tasks(self, task_id, subtasks=[]):
        r.rpush(self.mykey + task_id, subtasks)
        
    def get_sub_tasks(self, task_id):
        subtask_list = r.lrange(self.mykey + task_id, 0, r.llen(self.mykey + task_id))
        return subtask_list

