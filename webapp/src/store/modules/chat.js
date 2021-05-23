import apiClient from '../../providers/api'
import chatServices from '../../services/chat'
import Message from '../../models/Message'

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
    state.messages.push(new Message(msg))
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
    messages.results = messages.results.map(message => new Message(message))
    if(messages.first_time)
      state.messages = [...messages.results]
    else
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
    const statusConnection = chatServices.statusConnectionByRoom({ vm, room })
    
    const socketIsOpen = statusConnection.socketIsOpen
    const isTheSameRoom = statusConnection.isTheSameRoom

    if(socketIsOpen && isTheSameRoom){
        return
    }

    if (socketIsOpen && !isTheSameRoom) {
      console.log('Closing Old Chat WS service')
      chatServices.closeSocketService()
      commit('clearMessages')
    }
    
    const callback = message => dispatch('onMessage', message.data)
    chatServices.setSocketService({ vm, url, callback })
  },
  onMessage ({ commit }, message) {
    message = JSON.parse(message)
    console.log('HOLAAA',message)
    if (message.type === 'chat.message') commit('addMessage', message)
  },
  async getMessagesByRoom ({ commit }, payload) {
    const { data } = await apiClient.chat.getMessages(payload.id)
    console.log("antes deee",data)
    data.first_time = payload.first_time
    
    console.log('getMessagesByRoom')
    console.log(data)
    commit('unshiftMessages', data)
  },
  async getMessagesByUser ({ commit, dispatch }, payload) {
    const { data } = await apiClient.chat.getRoomByUserID(payload.to)
    data.first_time = payload.first_time
    dispatch('getMessagesByRoom', data)
    dispatch('connectToRoom', { vm: this.$app, room: data.id })
  },
  async getNextMessages ({ commit }) {
    const { data } = await apiClient.chat.getMessagesFromUrl(state.next)

    commit('blockScroll')
    commit('unshiftMessages', data)
    commit('unBlockScroll')
  },
  async sendChatMessage ({ commit, state, dispatch }, { msg }) {
    if(msg.files.length > 0){
      const { data } = await apiClient.chat.sendMessageWithFiles(state.room, msg)
      console.log("RESPUESTAA",data)
    }else{
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
}

export default {
  state,
  mutations,
  actions
}
