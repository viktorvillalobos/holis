import apiClient from '../../providers/api'
import chatServices from '../../services/chat'


const socketChat = process.env.NODE_ENV === 'production'
  ? `wss://${location.hostname}:${location.port}/ws/chat/`
  : `ws://${location.hostname}:${location.port}/ws/chat/`


const getChatUrlByRoomId = roomId => `${socketChat}${roomId}/`

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
  room: 'general',
  next: null,
  prev: null,
  currentChatID: null,
  chatActive: false
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
    commit('setRoom', room)

    const url = getChatUrlByRoomId(room)
    const mustCloseActiveConnection = chatServices.mustCloseActiveConnectionByRoom({ vm, room })

    if (mustCloseActiveConnection) {
      console.log('Closing Old Chat WS service')
      chatServices.closeSocketService()
      commit('clearMessages')
    }

    const callback = message => dispatch('onMessage', message.data)
    chatServices.setSocketService({ vm, url, callback })
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
    const payload = {
      type: 'chat.message',
      message: msg.message,
      room: state.room,
      to: state.currentChatID,
      is_one_to_one: true
    }

    window.$socketChat.sendObj(payload)
    const isRecent = state.recents.filter(x => x.id === state.currentChatID)

    if (!isRecent.length) dispatch('getRecents')
  }
}

export default {
  state,
  mutations,
  actions
}
