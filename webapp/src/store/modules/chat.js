import apiClient from '../../services/api'

const state = {
  users: [],
  connected: false,
  lastRooms: [],
  messages: [],
  recents: [],
  activeChat: null,
  asideOpen: false,
  allowScrollToEnd: true,
  currentChatName: 'Juaning Juan Harry',
  socketGrid: process.env.NODE_ENV === 'production'
    ? `wss://${location.hostname}:${location.port}`
    : `ws://${location.hostname}:${location.port}`,
  socketChat: process.env.NODE_ENV === 'production'
    ? `wss://${location.hostname}:${location.port}/chat/`
    : `ws://${location.hostname}:${location.port}/chat/`,
  room: 'general',
  next: null,
  prev: null,
  currentChatID: null,
  chatActive: false
}

const getters = {
  chatUrl (state) {
    return `${state.socketChat}${state.room}/`
  }
}

const mutations = {
  setChatActive (state, status) {
    state.chatActive = status
  },
  setRoom (state, name) {
    state.room = name
  },
  setCurrentChatName (state, name) {
    state.currentChatName = name
  },
  setCurrentChatID (state, userId) {
    state.currentChatID = userId
  },
  setRecents (state, recents) {
    state.recents = recents
  },
  blockScroll (state) {
    state.allowScrollToEnd = false
  },
  unBlockScroll (state) {
    state.allowScrollToEnd = true
  },
  setUsers (state, list) {
    state.users = list
  },
  setChatConnected (state, value) {
    state.connected = value
  },
  addMessage (state, msg) {
    state.messages.push(msg)
  },
  setMessages (state, lst) {
    state.messages = lst
  },
  addTempMessage (state, msg) {
    state.tempMessages.push(msg)
  },
  clearTempMessages (state) {
    state.tempMessages = []
  },
  unshiftMessages (state, messages) {
    state.messages = [...messages.results, ...state.messages]
    state.next = messages.next
    state.prev = messages.previous
  },
  clearMessages (state) {
    state.messages = []
  },
  setActiveChat (state, jid) {
    state.activeChat = jid
  },
  setAsideChat (state) {
    state.asideOpen = !state.asideOpen
    if (!state.asideOpen) state.activeChat = null
  }
}

const actions = {
  async getUsers ({ commit }) {
    const { data } = await apiClient.chat.getUsers()
    commit('setUsers', data.results)
  },
  async getRecents ({ commit }) {
    const { data } = await apiClient.chat.getRecents()
    commit('setRecents', data)
  },
  async connectToRoom ({ commit, state, getters, dispatch }, { vm, room }) {

    // const isTheSameUrl = window.$socketChat && window.$socketChatUrl.indexOf(getters.chatUrl) !== -1
    const socketIsOpen = window.$socketChat && window.$socketChat.readyState === 1

    const mustCloseActiveConnection = socketIsOpen // && isTheSameUrl

    if (mustCloseActiveConnection) {
      vm.$disconnect()
      commit('clearMessages')
    }

    commit('setRoom', room)

    vm.$connect(getters.chatUrl, {
      format: 'json',
      reconnection: true,
      connectManually: true,
      reconnectionDelay: 3000
    })

    window.$socketChat = vm.$socket

    window.$socketChat.onmessage = message => dispatch('onMessage', message.data)
  },
  onMessage ({ commit }, message) {
    message = JSON.parse(message)
    console.log(message)
    if (message.type === 'chat.message') commit('addMessage', message)
  },
  async getMessagesByRoom ({ commit }, room) {
    const { data } = await apiClient.chat.getMessages(room)

    console.log('getMessagesByRoom')
    console.log(data)
    commit('unshiftMessages', data)
  },
  async getMessagesByUser ({ commit, dispatch }, to) {
    const { data } = await apiClient.chat.getRoomByUserID(to)

    dispatch('getMessagesByRoom', data.id)
    dispatch('connectToRoom', { vm: this.$app, room: data.id })
  },
  async getNextMessages ({ commit }) {
    const { data } = await apiClient.chat.getMessagesFromUrl(state.next)

    commit('blockScroll')
    commit('unshiftMessages', data)
    commit('unBlockScroll')
  },
  sendChatMessage ({ commit, state, dispatch }, { msg }) {
    window.$socketChat.sendObj({ type: 'chat.message', message: msg.message, room: state.room })
    const isRecent = state.recents.filter(x => x.id === state.currentChatID)

    if (!isRecent.length) dispatch('getRecents')
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
