import React, { useState, useEffect } from 'react';

import Login from './components/Login/Login';
import Home from './components/Home/Home';
import MainHeader from './components/MainHeader/MainHeader';
import { getWSService } from "./services/WebSocket";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn');

    if (isLoggedIn === '1') {
      console.log("App Login!!!")
      setIsLoggedIn(true);
      connect();
    }
  }, []);

  const connect = () => {
    getWSService().sendMessage('connect', {'userId': localStorage.getItem('Username')})
  }

  const loginHandler = (username) => {
    localStorage.setItem('isLoggedIn', '1');
    localStorage.setItem('Username', username);
    setIsLoggedIn(true);
    connect();
  };

  const logoutHandler = (username) => {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('Username');
    setIsLoggedIn(false);
  };

  return (
    <React.Fragment>
      <MainHeader isAuthenticated={isLoggedIn} onLogout={logoutHandler} />
      <main>
        {!isLoggedIn && <Login onLogin={loginHandler} />}
        {isLoggedIn && <Home onLogout={logoutHandler} />}
      </main>
    </React.Fragment>
  );
}

export default App;
