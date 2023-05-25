import React, { useState, useEffect } from 'react';
import {getWSService} from '../services/WebSocket'

const ChatContext = React.createContext({
    isConnected: false,
    messages: [],
    username: '',
    onConnect: (user) => { },
    onDisconnect: () => { },
    sendMessage: (message) => {}
});

const wsService = getWSService()

export const ChatContextProvider = (props) => {
    const [isConnected, setIsConnected] = useState(localStorage.getItem('isLoggedIn') === '1');
    const [username, setUsername] = useState(localStorage.getItem('Username'));
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const isLoggedIn = localStorage.getItem('isLoggedIn');

        if (isLoggedIn === '1') {
            connect();
        }
    }, []);
    
    const connect = () => {
        wsService.initSocket()
        wsService.addMessageListener('message', (message) => {
            setMessages(prevMessages => [...prevMessages, {user: message.user, message: message.message}])
        })
    }

    const disconnect = () => {
        wsService.close()
    }

    const sendMessage = (message) => {
        wsService.sendMessage('default', {
            'user' : username,
            'message': message
        })
    }

    const connectHandler = (username) => {
        localStorage.setItem('isLoggedIn', '1');
        localStorage.setItem('Username', username);
        setIsConnected(true);
        setUsername(username)
        connect();
    };

    const disconnectHandler = (username) => {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('Username');
        setIsConnected(false);
        setUsername('');
        disconnect();
    };

    return (
        <ChatContext.Provider
            value={{
                isConnected: isConnected,
                messages: messages,
                username: username,
                sendMessage: sendMessage,
                onConnect: connectHandler,
                onDisconnect: disconnectHandler
            }}
        >
            {props.children}
        </ChatContext.Provider>
    );
};

export default ChatContext;