import socketServices from './sockets'

export default {
  setSocketService ({ vm, url, callback }, options) {
    window.$socketChat = socketServices.getSocketConnection({
      vm,
      url,
      callback
    }, options)
  },
  closeSocketService ({ vm }) {
    window.$socketChat.close()
    delete vm.protype.$socket
  },
  mustCloseActiveConnectionByUrl ({ url }) {
    if (!window.$socketChat) return false

    const isTheSameUrl = window.$socketChat && window.$socketChat.url.indexOf(url) !== -1
    const socketIsOpen = window.$socketChat && window.$socketChat.readyState === 1

    return socketIsOpen && !isTheSameUrl
  }
}
