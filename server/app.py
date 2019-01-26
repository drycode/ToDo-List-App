#!/Users/DanYoung/Documents/workspace/ToDoAgain/flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import redis

app = Flask(__name__)

redis_host = "localhost"
redis_port = 6379
redis_password = ""

@app.route("/redis_health")
def hello_redis():
    """Example Hello Redis Program"""
    try:
        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    
        r.set("msg:hello", "Hello Redis!!!")
        msg = r.get("msg:hello")
        return msg, 201        

    except Exception as e:
        return e, 201

# TODO: Redefine the tasks model, and create reusable collections of tasks
# TODO: Create a database of tasks / Implement Redis
# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web', 
#         'done': False
#     }
# ]
@app.route("/reddis/todo/api/v1.0/tasks", methods=["POST"])
def set_tasks_test():
    print(request.json)
    if not request.json or not 'title' in request.json:
        abort(400)
    else:
        try:
            # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
            # using the default encoding utf-8.  This is client specific.
            r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)       
            
            cat = request.json['category']
            hash_name = f"todos:{cat}:tasks"
            r.hsetnx(hash_name, request.json["title"], str(request.json))

            msg = r.hgetall(hash_name)
            return jsonify(msg), 201

        except Exception as e:
            return e, 201

@app.route("/get_test")
def get_tasks_test():
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    msg = r.hgetall('todos:Practice:tasks')
    return jsonify(msg), 201

# Creates a URI field instead of id so the client is seeing URIs instead of IDs
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

# TODO: Pagination argument
# TODO: Filter options. Think about rows with which to filter
# TODO: SEARCH
# GET request for all task items in Database
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
# @auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

# GET request for single task item in Database
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# @auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# POST request to add task item to database
# TODO: Don't allow duplicate tasks by Title
# TODO: Have a better system for incrementing IDs
# TODO: urls by title slug

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
# @auth.login_required
def create_task():
    # request will pass the data, but only if it came marked as JSON
    if not request.json or not 'title' in request.json:
        # returns error for bad request
        abort(400)
    task = {
        # manually auto incrementing task['id']
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        # defaulting description to none
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    # 201 code means successfully created
    return jsonify({'task': task}), 201


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