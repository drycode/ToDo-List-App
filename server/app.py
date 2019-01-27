#!/Users/DanYoung/Documents/workspace/ToDoAgain/flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import redis

app = Flask(__name__)

redis_host = "localhost"
redis_port = 6379
redis_password = ""

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)       

@app.route("/redis_health")
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

@app.route("/todo/api/v1.0/tasks", methods=["POST"])
# @auth.login_required
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
@app.route("/todo/api/v1.0/tasks/all")
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
@app.route("/todo/api/v1.0/tasks")
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
    print(request.json)
    cat = request.json['category']
    title = request.json['title']
    hash_name = f"todos:{cat}:tasks"
    msg = r.hget(hash_name, title)
    return jsonify(msg), 201



@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
# @auth.login_required
def update_task(task_id):
    print(request.json)
    # Find the task in the list of tasks
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    # Update task given parameters specified in request.json after confirming data is clean
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
# @auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

@app.errorhandler(404)
# @auth.login_required
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)