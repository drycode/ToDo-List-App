import React from "react";

const renderForm = ({ categories }) => {
  let items = [];
  for (let category in categories) {
    items.push(<option value={category}>{category}</option>);
  }
  return items;
};

export const CategorySelector = (categories, selectedCategory) => {
  return (
    <div>
      <select>
        {renderForm(categories).map(item => {
          return item;
        })}
      </select>
    </div>
  );
};
