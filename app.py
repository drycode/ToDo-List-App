#!./bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth, make_response

app = Flask(__name__)

# TODO: Create a user database (Redis)
# TODO: Setup Google SSO 
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# TODO: Redefine the tasks model, and create reusable collections of tasks
# TODO: Create a database of tasks / Implement Redis
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]


# Creates a URI field instead of id so the client is seeing URIs instead of IDs
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

# GET request for all task items in Database
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

# GET request for single task item in Database
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
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
@auth.login_required
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
@auth.login_required
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
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

@app.errorhandler(404)
@auth.login_required

def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)