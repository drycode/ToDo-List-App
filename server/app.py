#!/Users/DanYoung/Documents/workspace/ToDoAgain/flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, session, url_for, redirect
import json
import redis
from config.databaseconfig import *
import server.auth as auth
import os
from functools import wraps
import datetime
import jwt
import server.redis_methods as db

app = Flask(__name__)
app.secret_key = os.urandom(24)

r = redis.StrictRedis(host=rconf['REDIS_HOST'], port=rconf['REDIS_PORT'], password=rconf['REDIS_PASSWORD'], decode_responses=True)       

# Decorator function to ensure protected route handling
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session['oauth_state']:
            token = session['oauth_state']
        else:
            redirect("/login")	
        
        return f(*args, **kwargs)	
    return decorated

# TEST FUNCTIONS: DELETE LATER AFTER TESTING IMPLEMENTATION
@app.route("/getsession")
def getsession():
    return auth.getsession()
    
@app.route("/protected")
@token_required
def protected():
	return jsonify({'message':'This is only available for people with valid tokens'})

@app.route("/check_user")
@token_required
def show_user():
    return str(active_user)

@app.route("/redis_health", methods=['GET'])
@token_required
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
    json_obj['verified_email'] = str(json_obj['verified_email'])
    global active_user 
    active_user = db.ToDoUser(json_obj)
    print(active_user)
    return response

@app.route("/logout")
def logout():
    auth.logout()



# ROUTES
# WARNING: eval() mehod in this route flow. Secure requests on frontend

###################################################################################
@app.route("/redis/tasks", methods=["POST"])
# @token_required
def set_tasks():
    if not request.json:
        abort(400)
    else:
        try:
            for task in request.json:
                print(task)
                active_user.set_task(task)
            return str(request.json), 201
        except Exception as e:
            print("An exception was found")
            return e, 201

# DEPRECATED
@app.route("/todo/api/v1.0/tasks", methods=["POST"])
@token_required
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

###################################################################################
@app.route("/redis/tasks", methods=['GET'])
@token_required
def get_all_tasks():
    try:
        tasks = [task for task in active_user.get_all_tasks()]
        for task in tasks:
            print(task)
        return jsonify(tasks), 201

    except Exception as e:
        return e, 201

# DEPRECATED
@app.route("/todo/api/v1.0/tasks", methods=['GET'])
@token_required
def get_all_tasks_test():
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

###################################################################################
# GET request for all tasks in specific categories
@app.route("/redis/tasks/<category>", methods=['GET'])
@token_required
def get_tasks_cat(category):
    print(category)
    # try:
    tasks = [task for task in active_user.get_category_tasks(category)]
    for task in tasks:
        print(task)
    print(tasks)
    return jsonify(tasks), 201

    # except Exception as e:
    #     print("an exception has occurred")
    #     return e, 201

# DEPRECATED
@app.route("/todo/api/v1.0/tasks", methods=['GET'])
@token_required
def get_tasks_cat_test():
    print(request.json)
    msg = {}
    categories = request.json['category']
    for cat in categories:
        hash_name = f"todos:{cat}:tasks"
        task = r.hgetall(hash_name)
        msg.update(task)
    return jsonify(msg), 201

###################################################################################

# GET request for single task item in Database
@app.route('/todo/api/v1.0/tasks/<category>/<title>', methods=['GET'])
@token_required
def get_task(category, title):
    hash_name = f"todos:{category}:tasks"
    msg = r.hget(hash_name, title)
    return jsonify(msg), 201

###################################################################################

@app.route('/todo/api/v1.0/tasks/<category>/<title>/delete', methods=['DELETE'])
@token_required
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

###################################################################################

@app.errorhandler(404)
@token_required
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)



# TODO: Pagination argument
# TODO: SEARCH
