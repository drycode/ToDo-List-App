import React from "react";

class TaskItem extends React.Component {
  state = { selectedTask: false };

  componentDidUpdate() {
    console.log("I've been clicked");
    if (this.selectedTask) {
      this.renderDisplay();
    }
  }

  handleClick = () => {
    console.log(this.state.selectedTask);
    this.setState({ selectedTask: this.state.selectedTask ? false : true });
  };

  renderDisplay() {
    if (this.state.selectedTask) {
      return (
        <div onClick={this.handleClick}>
          <div className="title">{this.props.task.title}</div>
          <div className="due_date">{this.props.task.due_date}</div>
          <div className="category">Category: {this.props.task.category}</div>
        </div>
      );
    }
    return (
      <div onClick={this.handleClick}>
        <div className="title">{this.props.task.title}</div>
      </div>
    );
  }

  render() {
    return this.renderDisplay();
  }
}

// const TaskItem = ({ task }) => {
//   const displayDetails = isSelected => {
//     return isSelected ? true : false;
//   };

//   const renderSelectedTask = isSelected => {
//     if (isSelected) {
//       return <div className="dueDate">{task.date_created}</div>;
//     }
//     return <div>Hello</div>;
//   };

//   return (
//     <div onClick={() => displayDetails()}>
//       <div className="title">{task.title}</div>
//       {renderSelectedTask(onClick}
//     </div>
//   );
// };

export default TaskItem;
