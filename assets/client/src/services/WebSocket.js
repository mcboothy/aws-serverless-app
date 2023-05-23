import WebSocket from 'isomorphic-ws';

let WSService = null;

class WebSocketService {

  constructor() {    
    this.websocket = null;
    this.messageListeners = [];
    this.isOpen = false;
  }

  /**
   *  Set up WebSocket connection for a new user and
   *  basic listeners to handle events
   */
  initSocket = (user) => {    
    var loc = window.location, url;
    if (loc.protocol === "https:") {
      url = "wss:";
    } else {
      url = "ws:";
    }
    url += "//" + loc.host;
    url += loc.pathname + "wsprod/";    
    this.websocket = new WebSocket(url);
    this.websocket.onopen = this.onConnOpen;
    this.websocket.onmessage = this.onMessage;
    this.websocket.onclose = this.onConnClose;
  }

  close = () => {
    this.websocket.close();
  }

  /**
   *  Show connection status to user
   */
  onConnOpen = () => {
    this.isOpen = true;
    console.log('Websocket connected!');   
  }

  /**
   *  Log lost connection for now
   */
  onConnClose = () => {
    console.log('Websocket closed!');
  }

  /**
   *  Used by application to send message to the WebSocket API Gateway
   *  @param routeKey The route key for WebSocket API Gateway
   *  @param message String message
   *  message {
   *    room,
   *    type,
   *    msg,
   *    username,
   *    for
   *  }
   */
  sendMessage = (routeKey, message) => {    
    if(this.websocket && this.isOpen){
      this.websocket.send(JSON.stringify({
        route_key: routeKey,
        data: JSON.stringify(message)
      }));
    }else{      
      console.log(`Websocket connection not found!!`);
    }    
  }

  /**
   *  Used by application to register different listeners for 
   *  different message types [To be used later]
   *  @param type Message type ['all', 'pm']
   *  @param listener Function to handle message type
   */
  addMessageListener = (type, listener) => {    
    if (!type ||typeof listener !== 'function') {
      return;
    }
    this.messageListeners.push({
      type,
      listener
    });
  }

  /**
   * Handler that receives the actual messages from the WebSocket API
   * For now it simply returns the parsed message body
   * @param data Message body received from WebSocket 
   */
  onMessage = (data) => {
    console.log(data)
    if (data) {
      const message = JSON.parse(data.data);    
      const typeListener = this.messageListeners.find(listener => listener.type === message.type);

      if (typeListener && typeof typeListener.listener === "function") {      
        typeListener.listener(message);
      } else {
        console.log('No handler found for message type');
      }
    }
  }

  static initWSService() {    
    if (!WSService) {      
      WSService = new WebSocketService();
      WSService.initSocket();
      return WSService;
    }
    
    return WSService;
  }

}

export const getWSService = WebSocketService.initWSService;