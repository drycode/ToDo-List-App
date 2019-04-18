# ToDo List API

> This project features a robust Todo list REST API using Flask and Redis and a React/Redux front end.

![last-commit][last-commit]
![open-issues][open-url]
![coverage][coverage]

In an attempt to learn more about the use of a strict key/value store, I started creating ToDo task items in the Redis CLI. After a few hours of building different representations of task items, I decided to build out a full API in Flask. This repository reflects both that API project, and a React front end that I build to render it in the browser. 

## Installation

Be sure to first install the latest versions of [Python](https://www.python.org/downloads/) and [React](https://www.tutorialspoint.com/reactjs/reactjs_environment_setup.htm). 

Next by making a clone of this repository. 
```sh
~ mkdir todo-app
~ cd todo-app
~ git clone https://github.com/danyoungmusic93/ToDo-List-App
```

## Development setup

Because this repository is monolithic, be sure to create separate dependency management systems for the `./api` and `./client` directories. 

```sh
~ python -m virtualenv api
::virtual env output::
~ source bin/activate           //or another command to initiate virtual environment
~ (api) cd api
~ (api) pip install -r requirements.txt
~ (api) which python
/env/bin/python         // copy the path to the virtual environments version of python
```
This will install the primary dependencies for the Python/Flask API portion of our application. You will still need to set up some configuration files, and apply for an API key through [Google's OAuth API](https://developers.google.com/identity/protocols/OAuth2). Once you have your login credentials, be sure to save them in a configuration file at `/todo-app/api/server/authentication/google_api_config.py`. 

The copied PYTHONPATH will be added to the top of the `/todo-app/api/app.py` file in the following shebang format: `#!/env/bin/python`. This allows us to launch our Flask server with the following command and output:

```sh
~ (api) ./app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 490-370-085
```


Now lets move onto the client side of our application. 

```sh
~ (api) cd ..                 
~ (api) deactivate            // to deactivate the virtual environment  
~ cd client
~ npm install                 // installs nodemodules listed in package.json file
~ npm start

```

## REDIS Implementation
_-- Lower-level concepts for the datastructure minded._

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
