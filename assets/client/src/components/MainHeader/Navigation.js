import React, { useContext } from 'react';
import ChatContext from '../../store/chat-context';
import classes from './Navigation.module.css';

const Navigation = (props) => {
  const ctx = useContext(ChatContext);

  return (
    <nav className={classes.nav}>
      <ul>
        {ctx.isConnected && (
          <li>
            <button onClick={ctx.onDisconnect}>Logout</button>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Navigation;
