const state = {
  room: null, // Current room id
  connected: false,   // Connected to a room
  enableAudio: true,  // Activate audio in the current room
  enableVideo: false, /// Activate video in the current call
  muteAudio: false,   // mute my audio in the current call
  muteMicro: false,    // mute my micro in the current call
  status: 'disconnected'
}

const mutations = {
  setConnected(state, enable) {
    state.connected = enable
  },
  setRoom(state, room) {
    state.room = room
  },
  setEnableAudio(state) {
    state.enableAudio = !state.enableVideo
  },
  setEnableVideo(state) {
    state.enableVideo = !state.enableVideo
  },
  setMuteAudio(state, enable) {
    state.muteAudio = enable
  },
  setMuteMicro(state, enable) {
    state.muteMicro = enable
  },
  setStatusConnecting(state) {
    state.status = 'connecting'
  },
  setStatusConnected(state) {
    state.status = 'connected'
  },
  setStatusDisconnected(state) {
    state.status = 'disconnected'
  },

}

const actions = {
  disconnectAndConnect({ commit }, room) {
    commit("setConnected", false)
    commit("setStatusConnecting")

    setTimeout(() => { 
      commit("setConnected", true)
      commit("setRoom", room)
    }, 4000)

  },
  changeToVideo({ commit }) {
    commit("setEnableVideo")
    commit("setConnected", false)

    commit("setConnected", false)
    setTimeout(() => { 
      commit("setConnected", true)
    }, 4000)
  }
}

export default {
  state,
  mutations,
  actions
}

