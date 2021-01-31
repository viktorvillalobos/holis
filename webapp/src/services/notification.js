import socketServices from './sockets'

export default {
  setSocketService ({ vm, url, callback }, options) {
    const { observer, socket } = socketServices.getSocketConnection({
      url,
      callback,
      socketName: '$socketNotification'
    }, options)

    window.$socketNotification = socket
    window.$observerNotification = observer
  },
  closeSocketService () {
    window.$observerChat.reconnection = false
    window.$socketChat.close()
    delete window.$socketChat
  }
}
