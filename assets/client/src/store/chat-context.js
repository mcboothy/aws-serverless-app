import React, { useState, useEffect } from 'react';
import {getWSService} from '../services/WebSocket'

const ChatContext = React.createContext({
    isConnected: false,
    messages: [],
    onConnect: (user) => { },
    onDisconnect: () => { },
    sendMessage: (message) => {}
});

const wsService = getWSService()

export const ChatContextProvider = (props) => {
    const [isConnected, setIsConnected] = useState(false);
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const isLoggedIn = localStorage.getItem('isLoggedIn');

        if (isLoggedIn === '1') {
            setIsConnected(true);
            connect();
        }
    }, []);


    // {user: "John", message: "Hello buddy"},
    // {user: "Dave", message: "Wassup"},
    // {user: "John", message: "What ya doing?"},
    
    const connect = () => {
        wsService.initSocket()
        wsService.addMessageListener('message', (message) => {
            setMessages(prevMessages => [...prevMessages, message])
        })
    }

    const disconnect = () => {
        wsService.close()
    }

    const sendMessage = (message) => {
        wsService.sendMessage('default', {
            'user' : localStorage.getItem('Username'),
            'message': message
        })
    }

    const connectHandler = (username) => {
        localStorage.setItem('isLoggedIn', '1');
        localStorage.setItem('Username', username);
        setIsConnected(true);
        connect();
    };

    const disconnectHandler = (username) => {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('Username');
        setIsConnected(false);
        disconnect();
    };

    return (
        <ChatContext.Provider
            value={{
                isConnected: isConnected,
                messages: messages,
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