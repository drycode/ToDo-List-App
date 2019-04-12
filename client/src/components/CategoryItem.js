import React from "react";
import { connect } from "react-redux";
import { categoryTasks } from "../actions";

class CategoryItem extends React.Component {
  render() {
    return (
      <div>
        <div
          className="item"
          onClick={() => {
            return this.props.categoryTasks(this.props.category);
          }}
        >
          {this.props.category}
        </div>
      </div>
    );
  }
}

export default connect(
  null,
  { categoryTasks }
)(CategoryItem);
