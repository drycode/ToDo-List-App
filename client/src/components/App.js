import React from "react";
import "../App.css";
// import { BrowserRouter, Route } from "react-router-dom";
import TaskList from "./TaskList";
import Header from "./Header";
import NavBar from "./NavBar";
import TaskCreate from "./TaskCreate";

class App extends React.Component {
  render() {
    return (
      <div className="ui container">
        <Header />
        <div className="ui grid">
          <div className="three wide column">
            <NavBar />
          </div>

          <div className="eight wide column">
            <div className="header">
              <h1>Todo List</h1>
              <TaskCreate />
            </div>
            <div className="ui container" style={{ marginTop: "35px" }}>
              <TaskList />
            </div>
          </div>

          <div className="five wide column">
            <h1>SubTasks List</h1>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
