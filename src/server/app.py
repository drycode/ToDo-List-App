#!/Users/DanYoung/Envs/flask/bin/python

import datetime
from functools import wraps
import json
import os

from flask import (
    Flask,
    jsonify,
    abort,
    make_response,
    request,
    session,
    url_for,
    redirect,
)
from flask_session import Session

# from auth import 
from redis_local import r, redis
from redis_methods import ToDoUser

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis.from_url("127.0.0.1:6379")

sess = Session()
sess.init_app(app)


def _get_active_user():
    obj = auth.session.get("user_id", None)
    if obj:
        active_user = ToDoUser(obj)
    else:
        active_user = False
    print(active_user)
    return active_user


# Decorator function to ensure protected route handling
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not auth.session.get("user_id", False):
            print("Not logged in")
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated


# TEST FUNCTIONS
@app.route("/getsession")
def getsession():
    return auth.getsession()


@app.route("/protected")
@token_required
def protected():
    return jsonify({"message": "This is only available for people with valid tokens"})


@app.route("/check_user")
@token_required
def show_user():
    return str(_get_active_user())


@app.route("/redis_health", methods=["GET"])
def hello_redis():
    """Example Hello Redis Program"""
    try:
        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        r.set("msg:hello", "Hello Redis!!!")
        msg = r.get("msg:hello")
        return msg, 201

    except Exception as e:
        return e, 201


@app.route("/login")
def login():
    return auth.login()


@app.route("/callback/google", methods=["GET"])
def callback():
    """Returns active_user variable for future redis calls"""
    response = auth.callback()
    json_obj = response.json
    json_obj["verified_email"] = str(json_obj["verified_email"])
    return response


@app.route("/logout")
def logout():
    auth.logout()
    return redirect("/login")


# ROUTES
# WARNING: eval() method in this route flow. Secure requests on frontend

###################################################################################
@app.route("/redis/tasks", methods=["POST"])
@token_required
def set_tasks():
    if not request.json:
        abort(400)
    else:
        try:
            for task in request.json:
                print(task)
                _get_active_user().set_task(task)
            return str(request.json), 201
        except Exception as e:
            print("An exception was found")
            return e, 201

###################################################################################
@app.route("/redis/tasks", methods=["GET"])
@token_required
def get_all_tasks():
    try:
        tasks = [task for task in _get_active_user().get_all_tasks()]
        for task in tasks:
            print(task)
        return jsonify(tasks), 201

    except Exception as e:
        return e, 201


###################################################################################
# GET request for all tasks in specific categories
@app.route("/redis/tasks/<category>", methods=["GET"])
@token_required
def get_tasks_cat(category):
    print(category)
    # try:
    tasks = [task for task in _get_active_user().get_category_tasks(category)]
    for task in tasks:
        print(task)
    print(tasks)
    return jsonify(tasks), 201

    # except Exception as e:
    #     print("an exception has occurred")
    #     return e, 201



###################################################################################
@app.route("/redis/tasks/<category>/<title>", methods=["GET"])
@token_required
def get_task(category, title):
    print(category + " " + title)
    task = _get_active_user().get_one_task(title)
    return jsonify(task), 201


###################################################################################

# TODO: test in postman
@app.route("/redis/tasks/delete", methods=["DELETE"])
@token_required
def delete_task(title):
    _get_active_user().delete_one_task(request.json["title"])
    return redirect("/redis/tasks"), 201


###################################################################################
# TODO: test in postman
@app.route("/redis/tasks/delete", methods=["DELETE"])
@token_required
def delete_multiple_tasks():
    _get_active_user().delete_tasks_by_category(
        request.json["category"], request.json["task_ids"]
    )
    return get_all_tasks()


###################################################################################

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True)


# TODO: Pagination argument
# TODO: SEARCH
# TODO: Currently, you may or may not be able to have multiple 
    # tasks with the same ID in different categories. Going to cause
    # bugs in deletion 
# TODO: Memoize _get_active_user() ???