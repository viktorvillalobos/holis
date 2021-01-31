import Observer from '../providers/sockets/observer'

export default {
  getSocketConnection ({ url, callback, socketName }, options) {
    console.assert(url, 'You must define a socket url to get a connection')

    options = options || {
      format: 'json',
      reconnection: true,
      connectManually: true,
      reconnectionDelay: 3000
    }

    options.$setInstance = (wsInstance) => {
      window[socketName] = wsInstance
    }

    const observer = new Observer(url, options)
    const socket = observer.WebSocket
    socket.onmessage = callback
    return {
      observer,
      socket
    }
  }
}
