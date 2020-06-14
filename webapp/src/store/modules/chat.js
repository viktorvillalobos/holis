import apiClient from '../../services/api'
import { client, xml } from "@xmpp/client"
import debug from "@xmpp/debug"

const state = {
  account: {
    service: "ws://localhost:7070/ws/",
    domain: "holis.local",
    resource: "webapp",
    username: "admin",
    password: "",
  },
  xmpp: null,
  users: [],
  channels: [],
  connected: false
}

const mutations = {
  setUsers(state, list) {
    state.users = list
  },
  setChannels(state, list) {
    state.channels = list
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
}

const actions = {
  async getUsers({ commit }) {
    const {data} = await apiClient.chat.getUsers()
    console.log(data)
    commit('setUsers', data.results)
  },
  async getChannels({ commit }) {
    const {data} = await apiClient.chat.getChannels()
    console.log(data)
    commit('setChannels', data)
  },
  /* eslint-disable */
  async connectXMPP ({ commit, dispatch }, isDev) {
    const { data } = await apiClient.chat.getCredentials()

    await commit('setAccount', {
      service: "ws://localhost:7070/ws/",
      domain: "holis.local",
      resource: "webapp",
      username: data.jid,
      password: data.token,
    })

    console.log(data)
    const xmpp = client(state.account)

    xmpp.on("error", (err) => dispatch('onError', err))

    xmpp.on("offline", () => dispatch('onDisconnected'))

    xmpp.on("stanza", async (stanza) => dispatch('onStanza', stanza))

    xmpp.on("online", async (address) => dispatch("setUserOnline", address ))

    window.$xmpp = xmpp
    window.$xml = xml

    try {
      await window.$xmpp.start()
      console.log('Connected to XMPP')
     // commit('setXMPP', { isDev, xmpp })
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
  async setUserOnline({ state }, address) {
      // Makes itself available
      await window.$xmpp.send(xml("presence"));

      // Sends a chat message to itself
      const message = xml(
        "message",
        { type: "chat", to: 'admin@holis.local' },
        xml("body", {}, "hello world"),
      )
      await window.$xmpp.send(message)

    },
  onStanza({ commit }, stanza) {
      console.log(stanza)
      if (stanza.is("message")) {
        // await xmpp.send(xml("presence", { type: "unavailable" }));
        // await xmpp.stop();
      }
    }
}

export default {
  state,
  mutations,
  actions
}
