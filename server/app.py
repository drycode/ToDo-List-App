#!/Users/DanYoung/Documents/workspace/ToDoAgain/flask/bin/python

import datetime
from functools import wraps
import json
import os

from flask import Flask, jsonify, abort, make_response, request, session, url_for, redirect

from config.databaseconfig import *
import server.auth as auth
from server.redis_local import r
import server.redis_methods as db

app = Flask(__name__)

app.secret_key = os.urandom(24)

active_user = False

def _set_active_user(active_user): 
    obj = session.get('user_id', None)
    if obj:
        active_user = db.ToDoUser(obj)
    else:
        active_user = False
    print(active_user)

# Decorator function to ensure protected route handling
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        _set_active_user(active_user)
        # user_session = session.get('user_id', None)
        if not session.get('user_id', False):
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
    # _redis_session_store(auth.session)
    return response

@app.route("/logout")
def logout():
    auth.logout()
    return redirect('/login')

    



# ROUTES
# WARNING: eval() mehod in this route flow. Secure requests on frontend

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

@app.route("/redis/tasks/<category>/<title>/delete", methods=['DELETE'])
@token_required
def delete_task(category, title):
    print(category + title)
    # try:
    active_user.delete_tasks_by_category(category, active_user._blake2b_hash_title(title))
    return redirect('/redis/tasks'), 201
    # except:
        # msg = {"msg":"Invalid deletion parameters. Please try again."}
        # return jsonify(msg)
    
# DEPRECATED
@app.route('/todo/api/v1.0/tasks/<category>/<title>/delete', methods=['DELETE'])
@token_required
def delete_task_test(category, title):
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
# TODO: implement multi-delete
@app.route('/redis/tasks', methods=['DELETE'])
@token_required
def delete_multiple_tasks():
    active_user.delete_tasks_by_category(request.json['category'], request.json['task_ids'])
    return get_all_tasks()

###################################################################################
# Possibly Deprecated.....
def _redis_session_store(session):
    auth.session['session_id'] = active_user.get_user_id()
    hash_key = "session_data:{}:session_info".format(auth.session['session_id'])
    r.hset(hash_key, "access_token", auth.session['oauth_state']['access_token'])
    r.hset(hash_key, "id_token", auth.session['oauth_state']['id_token'])
    r.expire(hash_key, int(auth.session['oauth_state']['expires_in']))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)



# TODO: Pagination argument
# TODO: SEARCH
