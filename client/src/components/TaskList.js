import React, { Component } from "react";
import { connect } from "react-redux";
import { fetchTasks } from "../actions";
import TaskItem from "./TaskItem";

class TaskList extends Component {
  componentDidMount() {
    this.props.fetchTasks();
  }

  renderTasks = tasks => {
    if (tasks.length > 0) {
      return (
        <div className="ui middle aligned animated selection divided list">
          {tasks.map(task => {
            return (
              // TODO:  Get task id for Key from api using action creator

              <div className="item">
                <TaskItem task={task} />
              </div>
            );
          })}
        </div>
      );
    }
  };
  render() {
    return <div>{this.renderTasks(this.props.tasks)}</div>;
  }
}

const mapStateToProps = state => {
  return { tasks: state.tasks };
};

export default connect(
  mapStateToProps,
  { fetchTasks }
)(TaskList);
