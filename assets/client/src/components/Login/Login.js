import React, { useReducer, useContext } from 'react';

import Card from '../UI/Card/Card';
import classes from './Login.module.css';
import Button from '../UI/Button/Button';
import ChatContext from '../../store/chat-context';

const stateReducer = (state, action) => {
  let newState = {...state}
  switch (action.type){
    case "USERNAME_CHANGED":
      newState.username = action.val;
    break;
  }

  newState.formIsValid = newState.username.trim().length > 4
  return newState
};

const Login = (props) => {
  const ctx = useContext(ChatContext);

  const [state, dispatchState] = useReducer(stateReducer, {
    username: '',
    formIsValid: false,
  });

  const userChangeHandler = (event) => {
    dispatchState({type: 'USERNAME_CHANGED', val: event.target.value})
  };

  const validateUserHandler = () => {
    dispatchState({type: 'USERNAME_BLUR'})
  };

  const submitHandler = (event) => {
    event.preventDefault();
    ctx.onConnect(state.username);
  };

  return (
    <Card className={classes.login}>
      <form onSubmit={submitHandler}>
        <div
          className={`${classes.control} ${
            state.formIsValid === false ? classes.invalid : ''
          }`}
        >
          <label htmlFor="user">Name</label>
          <input
            type="text"
            id="user"
            value={state.username}
            onChange={userChangeHandler}
            onBlur={validateUserHandler}
          />
        </div>
        <div className={classes.actions}>
          <Button type="submit" className={classes.btn} disabled={!state.formIsValid}>
            Enter
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default Login;
