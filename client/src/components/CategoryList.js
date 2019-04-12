import React from "react";
import { fetchCategories } from "../actions";
import { connect } from "react-redux";
import CategoryItem from "./CategoryItem";

class CategoryList extends React.Component {
  componentDidMount() {
    this.props.fetchCategories();
  }

  renderUniqueCategories = ({ categories }) => {
    if (categories) {
      return (
        <div className="ui middle aligned animated selection divided list">
          {[...new Set(categories)].map(category => {
            return (
              <div className="item">
                <CategoryItem category={category} />
              </div>
            );
          })}
        </div>
      );
    }
  };

  render() {
    return <div>{this.renderUniqueCategories(this.props.categories)}</div>;
  }
}

const mapStateToProps = state => {
  return { categories: state.categories };
};

export default connect(
  mapStateToProps,
  { fetchCategories }
)(CategoryList);
