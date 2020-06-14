import apiClient from '../../services/api'
import { client, xml } from "@xmpp/client"
import debug from "@xmpp/debug"

const state = {
  account: {
    service: "ws://localhost:7070/ws/",
    domain: "holis.local",
    resource: "webapp",
    username: "admin",
    password: "v21146023.",
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
  onError(state, error) {
    console.log(error)
  },
  onDisconnected(state)  {
    state.connected = false
    console.log('Disconnected from XMPP')
  },
  onConnected(state) {
    state.connected = true
    console.log('Connected to XMPP')
  }
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
  async connectXMPP ({ commit }, isDev) {
    const xmpp = client(state.account)

    xmpp.on("error", (err) => commit('onError', err));

    xmpp.on("offline", () => commit('onDisconnected'))

    xmpp.on("stanza", async (stanza) => {
      console.log(stanza)
      if (stanza.is("message")) {
        // await xmpp.send(xml("presence", { type: "unavailable" }));
        // await xmpp.stop();
      }
    })

    xmpp.on("online", async (address) => {
      console.log(address)
      // Makes itself available
      await xmpp.send(xml("presence"));

      // Sends a chat message to itself
      const message = xml(
        "message",
        { type: "chat", to: 'viktor@holis.local' },
        xml("body", {}, "hello world"),
      );
      await xmpp.send(message);
    });
  
    try {
      await xmpp.start()
      console.log('Connected to XMPP')
      // commit('setXMPP', { isDev, xmpp })
    } catch(error) {
      console.error(error)
    }

  }
}

export default {
  state,
  mutations,
  actions
}
