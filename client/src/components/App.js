import React from "react";
import "../App.css";
import TaskList from "./TaskList";
import Header from "./Header";
import NavBar from "./NavBar";

class App extends React.Component {
  render() {
    return (
      <div className="ui container">
        <Header />
        <div className="ui grid">
          <div className="two wide column">
            <NavBar />
          </div>
          <div className="eight wide column">
            <div className="header">
              <h1>Todo List</h1>
            </div>
            <TaskList />
          </div>
          <div className="six wide column">
            <h1>SubTasks List</h1>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
