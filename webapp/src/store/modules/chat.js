import apiClient from '../../services/api'
import * as XMPP from 'stanza'

const IS_PRODUCTION = process.env.NODE_ENV === 'production'


const state = {
  users: [],
  connected: false,
  lastRooms: [],
  messages: [],
  tempMessages: [],
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
  room: 'general'
}

const getters = {
  chatUrl (state) {
      return `${state.socketChat}${state.room}/`
  }
}

const mutations = {
  setRoom (state, name) {
    state.room = name
  },
  setCurrentChatName (state, name) {
    state.currentChatName = name
  },
  setCurrentChatJID (state, jid) {
    state.currentChatJID = jid
  },
  setLastBatch (state, batch) {
    state.lastBatch = batch
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
  unshiftMessage (state, msg) {
    state.messages.unshift(msg)
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
    commit('setRoom', room)


    vm.$connect(getters.chatUrl, {
      format: 'json',
      reconnection: true,
      reconnectionDelay: 3000
    })
    window.$socketChat = vm.$socket

    window.$socketChat.onmessage = message => dispatch('onMessage', message.data)

    // esto deberia estar en su modulo
    vm.$connect(state.socketGrid, {
      store: vm.$store,
      format: 'json',
      reconnection: true,
      reconnectionDelay: 3000
    })
    window.$socketGrid = vm.$socket
  },
  onMessage ({ commit }, message) {
    message = JSON.parse(message)
    console.log(message)
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
