export default (state = [], action) => {
  switch (action.type) {
    case "FETCH_TASKS":
      return action.payload;
    default:
      return state;
  }
};
