import React from "react";
import { Field, reduxForm } from "redux-form";

class TaskCreate extends React.Component {
  renderInput({ input, placeholder }) {
    return <input type="text" placeholder={placeholder} {...input} />;
  }

  renderForm() {
    return (
      <form onSubmit={this.props.handleSubmit(this.onSubmit)}>
        <h4 style={{ textAlign: "left" }}>Create New Task</h4>
        <div className="ui fluid input">
          <Field
            name="title"
            component={this.renderInput}
            placeholder="Add a task..."
          />
          <div
            class="ui icon button"
            data-tooltip="Add an optional due date to your task"
          >
            <i class="calendar icon button" />
          </div>
        </div>
        <div className="ui fluid input">
          <Field
            name="category"
            component={this.renderInput}
            placeholder="...and a category"
          />
          {/* <Field name="due_date" component={this.renderInput} /> */}
          <button className="ui button primary">Submit</button>
        </div>
      </form>
    );
  }

  onSubmit(formValues) {
    console.log(formValues);
  }

  render() {
    return this.renderForm();
  }
}

export default reduxForm({
  form: "taskCreate"
})(TaskCreate);
