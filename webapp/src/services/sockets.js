export default {
  getSocketConnection ({ vm, url, callback }, options) {
    console.assert(url, 'You must define a socket url to get a connection')

    options = options || {
      format: 'json',
      reconnection: true,
      connectManually: true,
      reconnectionDelay: 3000
    }

    vm.$connect(url, options)
    const socket = vm.$socket
    socket.onmessage = callback

    return socket
  }
}
