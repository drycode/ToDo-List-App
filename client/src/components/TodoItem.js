import React from "react";

const TodoItem = ({ task }) => {
  return (
    <div>
      <div className="title">{task.title}</div>
      <div className="dueDate">{task.due_date}</div>
    </div>
  );
};

export default TodoItem;
