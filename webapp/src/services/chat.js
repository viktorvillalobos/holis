import socketServices from './sockets'

export default {
  setSocketService ({ vm, url, callback }, options) {
    const { observer, socket } = socketServices.getSocketConnection({
      url,
      callback,
      socketName: '$socketChat'
    }, options)

    window.$socketChat = socket
    window.$observerChat = observer
  },
  closeSocketService () {
    window.$observerChat.reconnection = false
    window.$socketChat.close()
    delete window.$socketChat
  },
  statusConnectionByRoom ({ room }) {
    console.log(`mustCloseActiveConnectionByRoom: ${room}`)
    if (!window.$socketChat) return false
    console.log(`socketChat current url ${window.$socketChat.url}`)

    const isTheSameRoom = window.$socketChat && window.$socketChat.url.indexOf(room) !== -1
    const socketIsOpen = window.$socketChat && window.$socketChat.readyState === 1

    console.log(`isTheSameRoom: ${isTheSameRoom}`)
    console.log(`socketIsOpen: ${socketIsOpen}`)

    return {
      "socketIsOpen": socketIsOpen,
      "isTheSameRoom": isTheSameRoom
    }
  }
}
