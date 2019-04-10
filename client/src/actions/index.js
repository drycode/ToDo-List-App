import axios from "axios";

export const fetchTasks = () => async dispatch => {
  const response = await axios.get("/redis/tasks");
  dispatch({
    type: "FETCH_POSTS",
    payload: response
  });
};

export const createTask = formValues => async dispatch => {
  axios.post("/redis/tasks", formValues);
};
