import React, {useState, useContext, useRef } from 'react';

import Card from '../UI/Card/Card';
import Button from '../UI/Button/Button';
import classes from './Home.module.css';
import ChatContext from '../../store/chat-context';

const Home = (props) => {
  const ctx = useContext(ChatContext);
  const inputElement = useRef();

  const submitHandler = (event) => {
    event.preventDefault();
    ctx.sendMessage(inputElement.value);
  };

  return (
    <React.Fragment>
    <Card className={classes.home}>
      <form onSubmit={submitHandler}>
        <div
          className={classes.control}
        >
          <label htmlFor="user">Message</label>
          <input
            type="text"
            id="user"
            ref={inputElement}
          />

          <Button type="submit" className={classes.btn}>
            Send
          </Button>
        </div>
      </form>
    </Card>
    <ul>
      {ctx.messages.map(message => {
        return <Card>
          <div style={{position: 'relative', width: '100%', padding: '1rem'}}>
            <div style={{margin: '0.35rem'}}>
              {message.user}
            </div>
            <div style={{margin: '0.35rem'}}>
              {message.message}
            </div>            
          </div>          
        </Card>
      })}
    </ul>
    </React.Fragment>

  );
};

export default Home;
