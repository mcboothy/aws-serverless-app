import React, { useState, useContext, useEffect } from 'react';

import Login from './components/Login/Login';
import Home from './components/Home/Home';
import MainHeader from './components/MainHeader/MainHeader';
import ChatContext from './store/chat-context';

function App() {
  const ctx = useContext(ChatContext);

  return (
    <React.Fragment>
      <MainHeader />
      <main>
        {!ctx.isConnected && <Login />}
        {ctx.isConnected && <Home />}
      </main>
    </React.Fragment>
  );
}

export default App;
