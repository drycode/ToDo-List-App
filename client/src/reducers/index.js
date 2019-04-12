import { combineReducers } from "redux";
import { reducer as formReducer } from "redux-form";
import tasksReducer from "./tasksReducer";
import categoryReducer from "./categoryReducer";

export default combineReducers({
  tasks: tasksReducer,
  form: formReducer,
  categories: categoryReducer
});
