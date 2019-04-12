import {
  SIGN_IN,
  SIGN_OUT,
  FETCH_TASKS,
  FETCH_TASK,
  CREATE_TASK,
  DELETE_TASK,
  CATEGORY_TASKS
} from "../actions/types";

export default (state = {}, action) => {
  switch (action.type) {
    case FETCH_TASK:
      return { ...state, [action.payload.key]: action.payload };
    case FETCH_TASKS:
      return action.payload;
    case CREATE_TASK:
      return { ...state, [action.payload.title]: action.payload };
    case CATEGORY_TASKS:
      return action.payload;
    default:
      return state;
  }
};
