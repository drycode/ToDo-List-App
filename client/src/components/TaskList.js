import React, { Component } from "react";
import { connect } from "react-redux";
import { fetchTasks } from "../actions";
import TaskItem from "./TaskItem";

class TaskList extends Component {
  componentDidMount() {
    this.props.fetchTasks();
  }

  renderTasks = tasks => {
    console.log(tasks);
    if (tasks) {
      return (
        <div>
          <div>
            <ul>
              {tasks.map(task => {
                return (
                  // TODO:  Get task id for Key from api using action creator

                  <li className="task">
                    {task.category}
                    <TaskItem task={task} />
                  </li>
                );
              })}
            </ul>
          </div>
        </div>
      );
    }
  };
  render() {
    return <div>{this.renderTasks(this.props.tasks.data)}</div>;
  }
}

const mapStateToProps = state => {
  return { tasks: state.tasks };
};

export default connect(
  mapStateToProps,
  { fetchTasks }
)(TaskList);
