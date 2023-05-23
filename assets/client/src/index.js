import React from 'react';
import ReactDOM from 'react-dom/client';

import './index.css';
import App from './App';
import { ChatContextProvider } from './store/chat-context';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <ChatContextProvider>
      <App />
    </ChatContextProvider>
  );
