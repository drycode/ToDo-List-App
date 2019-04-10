import { combineReducers } from "redux";
import { reducer as formReducer } from "redux-form";
import tasksReducer from "./tasksReducer";

export default combineReducers({
  tasks: tasksReducer,
  form: formReducer
});
