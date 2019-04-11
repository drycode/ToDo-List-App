import React from "react";
import { Field, reduxForm } from "redux-form";
import { connect } from "react-redux";
import { createTask } from "../actions";

class TaskCreate extends React.Component {
  renderError = ({ error, touched }) => {
    if (touched && error) {
      return (
        <div className="ui mini error message">
          <div className="header">{error}</div>
        </div>
      );
    }
  };

  renderInput = ({ input, placeholder, meta }) => {
    return (
      <>
        <div className="ui fluid input">
          <input
            type="text"
            placeholder={placeholder}
            {...input}
            autoComplete="off"
          />
          <div
            className="ui icon button"
            data-tooltip="Add an optional due date to your task"
          >
            <i class="calendar icon button" />
          </div>
        </div>
        {this.renderError(meta)}
      </>
    );
  };
  renderCategoryInput = ({ input, placeholder, meta }) => {
    return (
      <>
        <div className="ui fluid input">
          <input
            type="text"
            placeholder={placeholder}
            {...input}
            autoComplete="off"
          />
        </div>
        {this.renderError(meta)}
        <button className="ui button primary" style={{ float: "right" }}>
          Submit
        </button>
      </>
    );
  };

  renderForm() {
    return (
      <form
        className="ui form error"
        onSubmit={this.props.handleSubmit(this.onSubmit)}
      >
        <h4 style={{ textAlign: "left" }}>Create New Task</h4>
        <Field
          name="title"
          component={this.renderInput}
          placeholder="Add a task..."
        />
        <Field
          name="category"
          component={this.renderCategoryInput}
          placeholder="...and a category"
        />
        {/* <Field name="due_date" component={this.renderInput} /> */}
      </form>
    );
  }

  onSubmit = formValues => {
    this.props.createTask(formValues);
  };

  render() {
    return this.renderForm();
  }
}

const validate = formValues => {
  const errors = {};
  if (!formValues.title) {
    errors.title = "You must enter a title";
  }
  if (!formValues.category) {
    errors.category = "You must enter a category";
  }

  return errors;
};

const formWrapped = reduxForm({
  form: "taskCreate",
  validate
})(TaskCreate);

export default connect(
  null,
  { createTask }
)(formWrapped);
