import React from "react";
import { CategoryList } from "./CategoryList";

class NavBar extends React.Component {
  render() {
    return (
      <div>
        <div>
          <h1>NavBar</h1>
        </div>
        <CategoryList />
      </div>
    );
  }
}
export default NavBar;
