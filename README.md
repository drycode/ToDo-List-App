# ToDo List API

> This project is a fairly standard ToDo list CRUD API using Flask and Redis.

![last-commit][last-commit]
![open-issues][open-url]
![coverage][coverage]

In an attempt to learn more about the use of a strict key/value store, I started creating ToDo task items in the Redis CLI. After a few hours of building different representations of task items, I decided to build out a full API in Flask.

## Installation

Be sure to setup a virtual environment to manage dependencies.

```sh
~ python -m virtualenv todo-app
~ cd todo-app
~ git clone https://github.com/danyoungmusic93/ToDo-List-App
```

## Development setup

```sh
~ source bin/activate
~ pip install -r requirements.txt
~ cd server
~ python app.py
```

## REDIS Implementation

#### Hashmap object storage

This project uses the Google OAuth2 API to allow for single sign-on, and stores the user's numerical Google ID in the Redis datastore. Task items are stored in a Redis hash, with a key containing both the user_id, and a unique task_id.

```sh
127.0.0.1:6379> hgetall key
127.0.0.1:6379> hgetall Todos:users:<user_id>:tasks:<task_id>
1) "title"
2) "Practice the saxophone"
3) "category"
4) "Freelance Work"
5) "date_created"
6) "20180502122411"
7) "due_date"
8) "20190209222411"
```

_-- Note that Python datetime objects have been converted to integers._

#### Sorted Set (hash_name, date_int, task_id)

The integer representation of dates allows for storage of task_ids in a sorted set for querying by date.

```sh
127.0.0.1:6379> zrange key start stop [WITHSCORES]
127.0.0.1:6379> zrange Todos:users:<user_id>:tasks:due_sort_all_task_ids 0 20190209222411
1) "0480a119a478b410bba4" (task_id1)
2) "55f1001e5afcdecd7a0a" (task_id2)
3) "fb4b0dc2756d5131a6f5" (task_id3)
```

_-- Task_ids are generated from `task_obj['title']` by using Python's built-in hashlib library to create a reversible 20 digit hashed number._

```sh
string = task_obj['title']

def _blake2b_hash_title(self, string):
        h = blake2b(digest_size=10)
        title = bytes(string, encoding="utf-8")
        h.update(title)
        task_id = h.hexdigest()
        return task_id
```

This Redis implementation sacrifices space for speed by creating multiple sets for different query parameters. For example, when querying tasks of a certain category, this set returns a collection of task_ids:

```sh
127.0.0.1:6379> smembers Todos:users:<user_id>:tasks:<category>:task_ids
1) "c5a0c4f15622e15ab4c7"
2) "55f1001e5afcdecd7a0a"
```

_-- These task_ids can then be used to query the hash map representation of the task object using hget as seen above._

[open-url]: https://img.shields.io/github/issues-raw/danyoungmusic93/todo-list-app.svg
[last-commit]: https://img.shields.io/github/last-commit/danyoungmusic93/todo-list-app.svg
[coverage]: ./api/coverage.svg
