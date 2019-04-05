import React, { Component } from "react";
import "../App.css";
import TodoList from "./TodoList";

class App extends Component {
  render() {
    return (
      <div className="container">
        <div className="header">
          <h1>Todo List</h1>
        </div>
        <TodoList />
      </div>
    );
  }
}

export default App;
