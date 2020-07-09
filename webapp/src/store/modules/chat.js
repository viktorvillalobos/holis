import apiClient from '../../services/api'
import * as XMPP from 'stanza'

const IS_PRODUCTION = process.env.NODE_ENV === 'production'

const WS_SERVER_URL = IS_PRODUCTION
  ? 'wss://bosh.chat.holis.chat/ws/'
  : 'ws://holis.local:7070/ws/'
const BOSH_SERVER_URL = IS_PRODUCTION
  ? 'wss://bosh.chat.holis.chat/http-bind/'
  : 'ws://holis.local:7070/http-bind/'

function compareJIDs (id1, id2) {
  try {
    const username = id1.split('@')[0]
    const username2 = id2.split('@')[0]
    return username === username2
  } catch {
    return false
  }
}

const state = {
  account: null,
  xmpp: null,
  users: [],
  connected: false,
  lastRooms: [],
  messages: [],
  activeChat: null,
  asideOpen: false,
  lastBatch: null
}

const getters = {
  JID (state) {
    const x = state.account
    return `${x.username}@${x.domain}/${x.resource}`
  }
}

const mutations = {
  setLastBach (state, batch) {
    state.lastBatch = batch
  },
  setUsers (state, list) {
    state.users = list
  },
  setAccount (state, account) {
    state.account = account
  },
  setXMPP (state, xmpp) {
    state.xmpp = xmpp
  },
  setChatConnected (state, value) {
    state.connected = value
  },
  addMessage (state, msg) {
    state.messages.push(msg)
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
    console.log(data)
    commit('setUsers', data.results)
  },
  async connectXMPP ({ commit, getters, dispatch }) {
    const { data } = await apiClient.chat.getCredentials()

    await commit('setAccount', {
      service: WS_SERVER_URL,
      domain: data.domain,
      resource: 'webapp',
      username: data.username,
      jid: data.jid,
      password: data.token
    })

    const client = XMPP.createClient({
      jid: getters.JID,
      password: state.account.password,
      transports: {
        websocket: WS_SERVER_URL,
        bosh: BOSH_SERVER_URL
      }
    })

    client.on('auth:success', () => dispatch('onAuthSuccess'))
    client.on('auth:failed', () => dispatch('onAuthFailed'))
    client.on('session:started', () => dispatch('onSessionStarted'))
    client.on('disconnect', () => dispatch('onDisconnect'))
    // client.on('chat', msg => dispatch('onChat', msg))
    client.on('iq', iq => dispatch('onIQ', iq))
    client.on('presence', e => dispatch('onPresence', e))
    client.on('stanza', e => dispatch('onStanza', e))

    client.connect()
    window.$xmpp = client
  },
  onStanza ({ commit, state, dispatch }, stanza) {
    console.log(stanza)
    if (stanza.archive && stanza.archive.item) {
      const item = stanza.archive.item
      const from = item.message.from.split('/')[0]
      const msg = {
        is_mine: state.account.jid === from,
        message: item.message.body,
        who: from.split('@')[0],
        datetime: item.delay.timestamp
      }
      commit('addMessage', msg)
    }

    if (stanza.type === 'chat') {
      dispatch('onChat', stanza)
    }
  },
  onError (error) {
    console.log(error)
  },
  onDisconnect ({ commit }) {
    commit('setChatConnected', false)
    console.log('Disconnected from XMPP')
  },
  onAuthSuccess ({ commit }) {
    commit('setChatConnected', true)
    console.log('XMPP: Connected')
  },
  onSessionStarted () {
    window.$xmpp.sendPresence()
  },
  onAuthFailed () {
    console.log('XMPP: Auth failed')
  },
  /* eslint-disable-next-line */
  onPresence({ state }, e) {
    // console.log('XMPP: Presence')
    // console.log(e)
  },
  async onChat ({ commit }, msg) {
    /* eslint-disable-next-line */
    console.log('XMPP: onChat')
    console.log(msg)
    if (!compareJIDs(msg.from, state.activeChat)) {
      alert(`Haz recibido un mensaje de ${msg.from}`)
    } else {
      commit('addMessage', { message: msg.body, is_mine: false, datetime: new Date() })
    }
  },
  /* eslint-disable-next-line */
  async onIQ ({ commit }, iq) {
    /* eslint-disable-next-line */
    console.log('XMPP: onIQ')
    console.log(iq)
  },
  async sendChatMessage ({ commit }, { to, msg }) {
    console.log(`sending msg to ${to}`)
    commit('addMessage', msg)
    await window.$xmpp.sendMessage({ to, body: msg.message, type: 'chat' })
  },
  async getMessages ({ commit, state }, jid) {
    commit('clearMessages')
    commit('setActiveChat', jid)
    const batch = await window.$xmpp.searchHistory(jid, {
      paging: {
        max: 20,
        before: state.lastBatch
      }
    })
    commit('setLastBach', batch)
  }
}

export default {
  state,
  getters,
  mutations,
  actions
}
