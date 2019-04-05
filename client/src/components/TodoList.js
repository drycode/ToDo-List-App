import React, { Component } from "react";
import TodoItem from "./TodoItem";
import axios from "axios";

class TodoList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      todos: [],
      categories: new Set()
    };
  }

  getTodos = () => {
    axios
      .get("/redis/tasks")
      .then(response => {
        this.setState({ todos: response.data });
      })
      .catch(error => console.log(error));
  };

  componentDidMount() {
    this.getTodos();
  }

  createTodo = async todo => {
    await axios.post("redis/tasks", { newTodo: { todo } });
    this.setState({
      todos: this.getTodos()
    });
  };

  // Not updating state
  sortByCategory = () => {
    let cats = new Set();
    this.state.todos.map(todo => {
      cats.add(todo.category);
      return cats;
    });
  };

  renderTasks() {
    if (this.state.todos.length > 0) {
      return (
        <div>
          <div>Form componenent for Adding Todo</div>
          <div className="listWrapper">
            <ul className="taskList">
              {this.sortByCategory()}
              {this.state.todos.map(todo => {
                return (
                  <li className="task" todo={todo} key={todo.id}>
                    {todo.category}
                    <TodoItem task={todo} />
                  </li>
                );
              })}
            </ul>
          </div>
        </div>
      );
    }
  }
  render() {
    return <div>{this.renderTasks()}</div>;
  }
}

export default TodoList;
