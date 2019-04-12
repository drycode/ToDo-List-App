import React from "react";
import CategoryList from "./CategoryList";

class NavBar extends React.Component {
  render() {
    return (
      <>
        <div className="header">
          <h1>NavBar</h1>
        </div>
        <CategoryList />
      </>
    );
  }
}
export default NavBar;
