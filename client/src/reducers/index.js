import { combineReducers } from "redux";
import tasksReducer from "./tasksReducer";

export default combineReducers({
  tasks: tasksReducer
});
