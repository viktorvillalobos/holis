import apiClient from '../../providers/api'
import chatServices from '../../services/chat'
import { Message, TempMessage } from '../../models/Message'
import moment from 'moment'
import ChatScreen from './../../models/chatScreen'

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
  inboxActive: false,
  screenChat: 'inbox'
}

const mutations = {
  setScreenChat (state, screnn) {
    state.screenChat = screnn
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
    const isTempMessage = msg.uuid === null
    const to_send = isTempMessage ? new TempMessage(msg) : new Message(msg)
    state.messages.push(to_send)
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
    const messagesAux = []
    var dateAux = ''

    messages.results = messages.results.map(message => new Message(message))
    const messagesFormatted = messages.first_time ? [...messages.results] :  [...messages.results, ...state.messages]

    console.log("TUNDIII",messagesFormatted)
    messagesFormatted.forEach(element => {
      const dateMomentAux = moment(element.created).format('L')
      if(dateAux != dateMomentAux){
        dateAux = dateMomentAux
        element.showDate = true
      }else
        element.showDate = false
      messagesAux.push(element)
    });

    state.messages = messagesAux
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
  async getUsers ({ commit }, search) {
    console.log("Entre2")
    const { data } = await apiClient.chat.getUsers(search)
    console.log("Entre4")
    commit('setUsers', data.results)
  },
  async getRecents ({ commit }, search) {
    const { data } = await apiClient.chat.getRecents(search)
    console.log(data)
    commit('setRecents', data)
  },
  async connectToRoom ({ commit, state, getters, dispatch }, { vm, room }) {
    commit('setRoom', room)

    const url = getChatUrlByRoomId(room)
    const statusConnection = chatServices.statusConnectionByRoom({ vm, room })

    const socketIsOpen = statusConnection.socketIsOpen
    const isTheSameRoom = statusConnection.isTheSameRoom

    if (socketIsOpen && isTheSameRoom) {
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
  onMessage ({ commit, state }, message) {
    message = JSON.parse(message)
    if (message.type === 'chat.message') {

      // Validate that is not a local sent message so, we not need to add again
      const existLocalMessage = state.messages.filter( x => x.app_uuid == message.app_uuid ).length > 0

      if (!existLocalMessage) commit('addMessage', message)
    }
  },
  async getMessagesByRoom ({ commit }, payload) {
    const { data } = await apiClient.chat.getMessages(payload.id)
    data.first_time = payload.first_time
    commit('unshiftMessages', data)
  },
  async getMessagesFromInbox ({ commit, dispatch }, payload) {
    //const { data } = await apiClient.chat.getRoomByGroup(payload)
    commit('setCurrentChatID', payload.id)
    dispatch('getMessagesByRoom', payload)
    dispatch('connectToRoom', { vm: this.$app, room: payload.id })
  },
  async getMessagesByChannel ({ commit, dispatch }, payload) {
    const { data } = await apiClient.chat.createChannel(payload)
    commit('setCurrentChatID', data.id)
    dispatch('getMessagesByRoom', data)
    dispatch('connectToRoom', { vm: this.$app, room: data.id })
  },
  async getMessagesByGroup ({ commit, dispatch }, payload) {
    const { data } = await apiClient.chat.getRoomByGroup(payload)
    commit('setCurrentChatID', data.id)
    dispatch('getMessagesByRoom', data)
    dispatch('connectToRoom', { vm: this.$app, room: data.id })
  },
  async getMessagesByUser ({ commit, dispatch }, payload) {
    const { data } = await apiClient.chat.getRoomByUserID(payload.to)
    data.first_time = payload.first_time
    if (payload.new_chat) {
      commit('setCurrentChatID', data.id)
    }
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
    const thereAreFiles = msg.files.length > 0

    let payloadSocketMessage = null

    if (thereAreFiles) {
      await chatServices.sendMessageWithFiles({
        room: state.room,
        msg
      })
    } else {
      payloadSocketMessage = chatServices.sendMessage({
        message: msg.message,
        room: state.room,
        to: state.currentChatID,
        is_one_to_one: true
      })
    }

    commit('addMessage', {
      avatar_thumb: null,
      created: new Date().toISOString(),
      room: payloadSocketMessage.room,
      app_id: payloadSocketMessage.app_uuid,
      text: payloadSocketMessage.message,
      user_id: null,
      user_name: 'Temp Message User',
      uuid: null,
      app_uuid: payloadSocketMessage.app_uuid,
      attachments: []
    })

    const isRecent = state.recents && state.recents.results.filter(x => x.id === state.currentChatID)
    if (!isRecent.length) dispatch('getRecents')
  }
}

export default {
  state,
  mutations,
  actions
}
