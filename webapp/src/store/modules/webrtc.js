const state = {
  room: 'tacata123.', // Current room id
  connected: false,   // Connected to a room
  enableAudio: true,  // Activate audio in the current room
  enableVideo: false, /// Activate video in the current call
  muteAudio: false,   // mute my audio in the current call
  muteMicro: false    // mute my micro in the current call
}

const mutations = {
  setConnected(state, enable) {
    state.connected = enable
  },
  setRoom(state, room) {
    state.room = room
  },
  setEnableAudio(state, enable) {
    state.enableAudio = enable
  },
  setEnableVideo(state, enable) {
    state.enableVideo = enable
  },
  setMuteAudio(state, enable) {
    state.muteAudio = enable
  },
  setMuteMicro(state, enable) {
    state.muteMicro = enable
  }
}

const actions = {

}

export default {
  state,
  mutations,
  actions
}

