import redis
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
        "date_due": "2-5-19"
    },
    {
        "title": "Play Saxophone", 
        "category": "Practice",
        "date_created": "2-3-19",
        "date_due": "2-5-19"
    }, 
    {
        "title": "Grocery Shop", 
        "category": "chores",
        "date_created": "2-3-19",
        "date_due": "2-5-19"
    }, 
    {
        "title": "Play Clarinet", 
        "category": "Practice",
        "date_created": "2-3-19",
        "date_due": "2-5-19"
    }
]


class ToDoTasks():    
    def __init__(self, userid):
        self.mykey = "Todos:users:" + str(userid) + ":"
        self.mytasks = self.mykey + ":tasks:"

    def set_task(self, task_obj):
        # Creates reversible hash that is reproducible by key
        h = blake2b(digest_size=10)
        title = bytes(task_obj['title'], encoding="utf-8")
        h.update(title)
        task_id = h.hexdigest()

        self.my_task_ids = self.mykey + ":task_ids"
        self.my_hash = self.mykey + str(task_id)

        r.hmset(self.my_hash, task_obj)
        r.sadd(self.mykey + task_obj['category'], task_id)
        r.sadd(self.my_task_ids, task_id)
    
    def get_all_tasks(self): 
        tasks = r.smembers(self.my_task_ids) 
        for task in tasks:
            result = r.hgetall(self.mykey  + task)
            print(result)
        


dan = ToDoTasks(123)
for task_obj in task_objs:
    dan.set_task(task_obj) 
dan.get_all_tasks()