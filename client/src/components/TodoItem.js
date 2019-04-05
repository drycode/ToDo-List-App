import React from "react";

const TodoItem = props => {
  return (
    <div>
      <input className="taskCheckbox" type="checkbox" />
      <label className="taskLabel">{props.task.title}</label>
      <div className="dueDate">{props.task.due_date}</div>
      <span className="deleteTaskBtn">DELETE BUTTON COMPONENT</span>
    </div>
  );
};

export default TodoItem;
