import redis
from datetime import datetime
from hashlib import blake2b

rconf = {
    'REDIS_HOST' : "localhost",
    'REDIS_PORT' : 6379,
    'REDIS_PASSWORD' : ""
}

r = redis.StrictRedis(host=rconf['REDIS_HOST'], port=rconf['REDIS_PORT'], password=rconf['REDIS_PASSWORD'], decode_responses=True)       

task_objs = [
    {
        "title": "Do your laundry", 
        "category": "chores",
        "date_created": "2-3-19",
        "due_date": datetime(2019, 2, 9, 22, 24, 11,346910)
    },
    {
        "title": "Play Saxophone", 
        "category": "Practice",
        "date_created": "2-3-19",
        "due_date": datetime(2019, 2, 9, 22, 24, 11,346911)
    }, 
    {
        "title": "Grocery Shop", 
        "category": "chores",
        "date_created": "2-3-19",
        "due_date": datetime(2019, 2, 9, 22, 24, 11,346912)
    }, 
    {
        "title": "Play Clarinet", 
        "category": "Practice",
        "date_created": "2-3-19",
        "due_date": None
    }
]

user_obj = {
    "email": "danyoungmusic93@gmail.com",
    "family_name": "Young",
    "given_name": "Daniel",
    "id": "115164965374312131232",
    "link": "https://plus.google.com/115164965374312131232",
    "locale": "en",
    "name": "Daniel Young",
    "picture": "https://lh3.googleusercontent.com/-f9bYxnccPbw/AAAAAAAAAAI/AAAAAAAAHz0/3a2v20L2HIo/photo.jpg",
    "verified_email": 'true'
}

class ToDoUser():    
    def __init__(self, user_obj):
        self.userid = user_obj['id']
        self.name = user_obj['given_name'] + " " + user_obj['family_name']
        self.mykey = "Todos:users:" + str(self.userid) + ":tasks:"
        r.hmset("Todos:users:" + str(self.userid), user_obj)
    """"All Create/Update functions will begin here and will continue through
    to the next explicit comment."""
    # Sets up all parts of the hash map

    def set_task(self, task_obj):
        """
        Establishes key value stores in redis for rapid querying of task_ids for specified
        queries. 

        Task_ids are used in subsequent queries for accessing hash map of specific task
        field data, 
        """
        # Creates reversible hash that is reproducible by key
        h = blake2b(digest_size=10)
        title = bytes(task_obj['title'], encoding="utf-8")
        h.update(title)
        task_id = h.hexdigest()
        task_obj['date_created'] = self._convert_datetime(datetime.utcnow())
        # Converts datetime object to integer value for sorting
        try:
            task_obj['due_date'] = self._convert_datetime(task_obj['due_date'])
            due_date = True
        except AttributeError:
            task_obj['due_date'] = str(None)
            due_date = False

        self.my_task_ids = self.mykey + "all_task_ids"
        self.task_hash = self.mykey + str(task_id)

        # Creates a hash_map of field value pairs for a particular user's task stored 
        # At location self.mykey:<task_id>. 
        # This hash will be queried for task data specific to a specific task_id
        r.hmset(self.task_hash, task_obj)

        # Stores all of the user's task_id keys
        # At location self.mykey:all_task_ids
        r.sadd(self.my_task_ids, task_id)        
        
        # Stores user's task_ids for a particular category
        # At location self.mykey:<category>_task_ids
        r.sadd(self.mykey + task_obj['category'] + "_task_ids", task_id)

        # Stores user's task_ids with due_date sorted by ascending order
        # print(task_obj['due_date'])
        if due_date:
            r.zadd(self.mykey + "due_sort_all_task_ids", { task_id: task_obj['due_date'] })
        
    """All Retrieval functions will begin here and will continue through to the next
    explicit comment."""
    
    # Queries all tasks
    def get_all_tasks(self):
        """
        Returns a generator object with hash results of all available task_ids.
        """ 
        tasks = r.smembers(self.my_task_ids) 
        for item in self._get_tasks(tasks):
            print(item)

    # Queries tasks by category
    def get_category_tasks(self, category):
        """
        Returns a generator object with hash results of task_id keys with given ``category``

        ``category`` should be passed as a string.
        """
        tasks = r.smembers(self.mykey + category + "_task_ids")
        for item in self._get_tasks(tasks):
            print(item)

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
            print(item)


    """Class based helper functions will begin here and will continue through to the next
    explicit comment."""
    # Creates integer value of datetime 
    def _convert_datetime(self, date):
        date = date.strftime("%Y%m%d%H%M%S")
        return int(date)
    
    def _stringify_datetime(self, date):
        year, month, day, hour, minute, second = map(int, (date[0:4], date[4:6], date[6:8], date[8:10], date[10:12], date[12:14]))
        date = datetime(year, month, day, hour, minute, second).strftime("Date: %m-%d-%Y Time: %H:%M:%S")
        return date

    def _get_tasks(self, tasks):
        return (r.hgetall(self.mykey + task) for task in tasks)




    """Dunder methods stored here."""
    def __repr__(self):
        tot_tasks = r.scard(self.my_task_ids)
        return "User(user_id: %r, name: %r, tasks: %r)" % (self.userid, self.name, tot_tasks)

    # def __iter__(self):


# TODO: implement real tests with unittest

# Tests
dan = ToDoUser(user_obj)
for task_obj in task_objs:
    dan.set_task(task_obj) 
print(dan)
# dan.get_all_tasks()
# dan.get_date_range(datetime(2019, 2, 9, 22, 24, 11,346910), datetime(2019, 2, 9, 22, 24, 14,346913))
# dan.get_category_tasks("Practice")
# convert_datetime()
