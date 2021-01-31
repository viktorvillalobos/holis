import Observer from '../providers/sockets/observer'

export default {
  getSocketConnection ({ vm, url, callback, socketName }, options) {
    console.assert(url, 'You must define a socket url to get a connection')

    options = options || {
      format: 'json',
      reconnection: true,
      connectManually: true,
      reconnectionDelay: 3000
    }

    options.$setInstance = (wsInstance) => {
      vm[socketName] = wsInstance
    }

    const socket = new Observer(url, options).WebSocket
    socket.onmessage = callback
    return socket
  }
}
