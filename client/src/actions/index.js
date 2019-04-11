import axios from "axios";
import {
  SIGN_IN,
  SIGN_OUT,
  FETCH_TASKS,
  FETCH_TASK,
  CREATE_TASK,
  DELETE_TASK,
  CATEGORY_TASKS
} from "./types";

export const signIn = () => async dispatch => {
  const response = await axios.get("/login");
  dispatch({
    type: SIGN_IN,
    payload: response
  });
};

export const signOut = () => async dispatch => {
  const response = await axios.get("/logout");
  dispatch({
    type: SIGN_OUT,
    payload: response
  });
};

export const fetchTasks = () => async dispatch => {
  const response = await axios.get("/redis/tasks");
  dispatch({
    type: FETCH_TASKS,
    payload: response.data
  });
};

export const fetchTask = (category, title) => async dispatch => {
  const response = await axios.get(`/redis/tasks/${category}/${title}`);
  dispatch({
    type: FETCH_TASK,
    payload: response
  });
};

export const createTask = formValues => async dispatch => {
  const response = await axios.post("/redis/tasks", formValues);
  console.log(response.data);
  dispatch({
    type: CREATE_TASK,
    payload: response.data
  });
};

export const deleteTask = title => async dispatch => {
  const response = await axios.delete("/redis/tasks/delete", title);
  dispatch({
    type: DELETE_TASK,
    payload: response
  });
};

export const categoryTasks = category => async dispatch => {
  const response = await axios.get(`/redis/tasks/${category}`);
  dispatch({
    type: CATEGORY_TASKS,
    payload: response
  });
};
