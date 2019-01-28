#!/Users/DanYoung/Documents/workspace/ToDoAgain/flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for, redirect
import json
import redis
from config.databaseconfig import *
import server.auth as auth

app = Flask(__name__)
app.secret_key = "super secret key"


r = redis.StrictRedis(host=rconf['REDIS_HOST'], port=rconf['REDIS_PORT'], password=rconf['REDIS_PASSWORD'], decode_responses=True)       

@app.route("/login")
def login():
    return auth.login()

@app.route("/callback/google", methods=["GET"])
def callback():
    response = auth.callback()
    json_obj = response.json
    dan = auth.User(json_obj) 
    print(dan)
    return response

@app.route("/logout")
def logout():
    auth.logout()

@app.route("/redis_health", methods=['GET'])
# @auth.login_required
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

# TODO: Redefine the tasks model, and create reusable collections of tasks
# TODO: Add date time

# @app.route("/todo/api/v1.0/authorize/google")
# def create_user(oauth_url):
#     redirect(oauth_url)

@app.route("/todo/api/v1.0/tasks", methods=["POST"])
def set_tasks_test():
    print(request.json)
    if not request.json or not 'title' in request.json or request.json['done']:
        abort(400)
    else:
        try:
            # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
            # using the default encoding utf-8.  This is client specific.
            cat = request.json['category']
            hash_name = f"todos:{cat}:tasks"
            r.hset(hash_name, request.json["title"], str(request.json))

            msg = r.hgetall(hash_name)
            return jsonify(msg), 201

        except Exception as e:
            return e, 201

# TODO: Pagination argument
# TODO: Filter options. Think about rows with which to filter
# TODO: SEARCH

# GET request for all task items in Database
@app.route("/todo/api/v1.0/tasks/all", methods=['GET'])
# @auth.login_required
def get_all_tasks():
    msg = {}
    categories = [cat for cat in r.scan_iter()]
    for hash_name in categories:
        print(hash_name)
        try:
            task = r.hgetall(hash_name)
            print(task)
            msg.update(task)
        except:
            pass
    return jsonify(msg), 201

# GET request for all tasks in specific categories
@app.route("/todo/api/v1.0/tasks", methods=['GET'])
# @auth.login_required
def get_tasks():
    print(request.json)
    msg = {}
    categories = request.json['category']
    for cat in categories:
        hash_name = f"todos:{cat}:tasks"
        task = r.hgetall(hash_name)
        msg.update(task)
    return jsonify(msg), 201

# GET request for single task item in Database
@app.route('/todo/api/v1.0/tasks/<category>/<title>', methods=['GET'])
# @auth.login_required
def get_task(category, title):
    # print(category + title)
    # cat = request.json['category']
    # title = request.json['title']
    hash_name = f"todos:{category}:tasks"
    msg = r.hget(hash_name, title)
    return jsonify(msg), 201

@app.route('/todo/api/v1.0/tasks/<category>/<title>/delete', methods=['DELETE'])
# @auth.login_required
def delete_task(category, title):
    hash_name = f"todos:{category}:tasks"
    if not r.hexists(hash_name, title):
        abort(404)
    try: 
        r.hdel(hash_name, title)
        msg = "Delete was successful"
    except:
        msg = "Something went wrong"
    return msg, 201

@app.errorhandler(404)
# @auth.login_required
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)