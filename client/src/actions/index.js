import axios from "axios";
import { CREATE_TASKS, FETCH_TASKS, SIGN_IN } from "./types";

export const fetchTasks = () => async dispatch => {
  const response = await axios.get("/redis/tasks");
  dispatch({
    type: FETCH_TASKS,
    payload: response
  });
};

export const createTask = formValues => async dispatch => {
  const response = await axios.post("/redis/tasks", formValues);
  dispatch({
    type: CREATE_TASKS,
    payload: response
  });
};

export const signIn = () => async dispatch => {
  const response = await axios.get("/login");
  dispatch({
    type: SIGN_IN,
    payload: response
  });
};
