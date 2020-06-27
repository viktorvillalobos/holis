import apiClient from '../../services/api'
import { client, xml } from "@xmpp/client"
import debug from "@xmpp/debug"

const IS_PRODUCTION = process.env.NODE_ENV == 'production'

const SERVER_URL = IS_PRODUCTION ? 'wss://holis.chat:7070/ws/' : 'ws://holis.local:7070/ws/'

const state = {
  account: null,
  xmpp: null,
  users: [],
  connected: false,
  lastRooms: [],
  messages: []
}

const mutations = {
  setUsers(state, list) {
    state.users = list
  },
  setAccount(state, account) {
    state.account = account
  },
  setXMPP(state, { xmpp, isDev }) {
    state.xmpp = xmpp
    if (isDev) debug(xmpp, true)
  },
  setConnected(state, value){
    state.connected = value
  },
  addMessage(state, msg) {
    state.messages.push(msg)
  },
  clearMessages(state) {
    state.messages = []
  }
}

const actions = {
  async getUsers({ commit }) {
    const {data} = await apiClient.chat.getUsers()
    console.log(data)
    commit('setUsers', data.results)
  },
  async connectXMPP ({ commit, dispatch }) {
    const { data } = await apiClient.chat.getCredentials()

    await commit('setAccount', {
      service: SERVER_URL,
      domain: "holis.local",
      resource: "webapp",
      username: data.jid,
      password: data.token,
    })

    const xmpp = client(state.account)
    window.$xmpp = xmpp
    window.$xml = xml

    window.$xmpp.on("error", (err) => dispatch('onError', err))
    window.$xmpp.on("offline", () => dispatch('onDisconnected'))
    window.$xmpp.on("stanza", async (stanza) => dispatch('onStanza', stanza))
    window.$xmpp.on("online", async (address) => dispatch("setUserOnline", address ))

    try {
      await window.$xmpp.start()
    } catch(error) {
      console.log(error)
    }

  },
  onError(error) {
    console.log(error)
  },
  onDisconnected({ commit })  {
    commit('setConnected', false)
    console.log('Disconnected from XMPP')
  },
  onConnected({ commit }) {
    commit('setConnected', true)
    console.log('Connected to XMPP')
  },
  async setUserOnline() {
    // Makes itself available
    await window.$xmpp.send(xml("presence"));
  },
  /* eslint-disable-next-line */
  onStanza({ commit }, stanza) {
    console.log(stanza)
    if (stanza.is("message")) {
      console.log("Te enviaron un mensaje")
      
      /* eslint-disable-next-line */
      if (true) {
        // If is the chat open
        const body = stanza.children.filter(x => x.name === 'body')[0]
        const text = body.children[0]
        commit('addMessage', { message: text, is_mine: false })
      }
      // await xmpp.send(xml("presence", { type: "unavailable" }));
      // await xmpp.stop();
    }
  },
  async sendChatMessage({ state, commit }, { to, msg }) {
    console.log(`sending msg to ${ to }`)

    commit('addMessage', msg)

    const message = xml(
      "message",
      { type: "chat", to: `${to}@${state.account.domain}`},
      xml("body", {}, msg.message),
    )

    await window.$xmpp.send(message)
  },
  async getMessages({ commit }, jid) {
    commit('clearMessages')
    console.log(`gettingMessages from ${ jid }}`)
  }
}

export default {
  state,
  mutations,
  actions
}
