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
  connected: false,
  lastRooms: []
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
      service: "ws://localhost:7070/ws/",
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
      // await xmpp.send(xml("presence", { type: "unavailable" }));
      // await xmpp.stop();
    }
  },
  /* eslint-disable-next-line */
  async sendChatMessage({ state, commit }, { to, msg }) {
    console.log(`sending msg to ${ to }`)
    const message = xml(
      "message",
      { type: "chat", to: `${to}@${state.account.domain}`},
      xml("body", {}, msg),
    )

    await window.$xmpp.send(message)
  }
}

export default {
  state,
  mutations,
  actions
}
