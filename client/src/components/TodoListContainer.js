import React, { Component } from "react";
import TodoItem from "./TodoItem";
import axios from "axios";
import { CategorySelector } from "./CategorySelector";

class TodoListContainer extends Component {
  state = {
    todos: [],
    categories: new Set(),
    selectedCategory: null
  };

  getTodos = async () => {
    const response = await axios.get("/redis/tasks");
    this.setState({
      todos: response.data
    });
    this.setState({
      categories: this.retrieveCategories()
    });
  };

  getByCategory = async event => {
    event.preventDefault();
    const response = await axios.get(
      `redis/tasks/${this.state.selectedCategory}`
    );
    this.setState({ todos: response.data });
  };

  componentDidMount() {
    this.getTodos();
  }

  retrieveCategories() {
    const categories = new Set();
    this.state.todos.map(todo => {
      categories.add(todo.category);
    });
    console.log(categories);
    return categories;
  }

  createTodo = async todo => {
    await axios.post("redis/tasks", { newTodo: { todo } });
    this.setState({
      todos: this.getTodos()
    });
  };

  handleChange = event => {
    this.setState({ selectedCategory: event.target.value });
  };

  renderTasks() {
    if (this.state.todos.length > 0 && this.state.categories) {
      return (
        <div>
          <div>
            <CategorySelector
              categories={this.state.categories}
              selectedCategory={this.state.selectedCategory}
            />
          </div>
          <div>
            <ul>
              {this.state.todos.map(todo => {
                return (
                  <div>
                    <li className="task" todo={todo} key={todo.id}>
                      {todo.category}
                      <TodoItem task={todo} />
                    </li>
                  </div>
                );
              })}
            </ul>
          </div>
        </div>
      );
    }
  }

  render() {
    console.log(this.state.categories);
    return <div>{this.renderTasks()}</div>;
  }
}

export default TodoListContainer;
