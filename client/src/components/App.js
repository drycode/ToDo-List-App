import React, { Component } from "react";
// import { BrowserRouter, Route } from "react-router-dom";
import "../App.css";
import TodoListContainer from "./TodoListContainer";
import Header from "./Header";

class App extends Component {
  render() {
    return (
      <div className="container">
        <Header />
        <div className="header">
          <h1>Todo List</h1>
        </div>
        <TodoListContainer />
      </div>
    );
  }
}

export default App;
