import React from "react";
import { Field, reduxForm } from "redux-form";

class TaskCreate extends React.Component {
  renderInput({ input, placeholder, meta }) {
    console.log(meta);
    return (
      <>
        <div className="ui fluid input">
          <input type="text" placeholder={placeholder} {...input} />
          <div
            className="ui icon button"
            data-tooltip="Add an optional due date to your task"
          >
            <i class="calendar icon button" />
          </div>
        </div>
        {/* <div>
          <div class="ui error message">
            <div class="header">{meta.error}</div>
          </div>
        </div> */}
      </>
    );
  }
  renderCategoryInput({ input, placeholder, meta }) {
    console.log(meta);
    return (
      <>
        <div className="ui fluid input">
          <input type="text" placeholder={placeholder} {...input} />
        </div>
        {/* <div>
          <div class="ui error message">
            <div class="header">{meta.error}</div>
          </div>
        </div> */}
        <button className="ui button primary" style={{ float: "right" }}>
          Submit
        </button>
      </>
    );
  }

  renderForm() {
    return (
      <form onSubmit={this.props.handleSubmit(this.onSubmit)}>
        <h4 style={{ textAlign: "left" }}>Create New Task</h4>
        <div>
          <Field
            name="title"
            component={this.renderInput}
            placeholder="Add a task..."
          />
        </div>
        <div>
          <Field
            name="category"
            component={this.renderCategoryInput}
            placeholder="...and a category"
          />
          {/* <Field name="due_date" component={this.renderInput} /> */}
        </div>
      </form>
    );
  }

  onSubmit(formValues) {
    // console.log(formValues);
  }

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

export default reduxForm({
  form: "taskCreate",
  validate
})(TaskCreate);
