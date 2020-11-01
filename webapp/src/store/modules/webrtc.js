const state = {
  room: null, // Current room id
  connected: false, // Connected to a room
  enableAudio: true, // Activate audio in the current room
  enableVideo: false, /// Activate video in the current call
  muteAudio: false, // mute my audio in the current call
  muteMicro: false, // mute my micro in the current call
  status: 'disconnected',
  disconnectByControl: false,
  streamsCount: 0,
  userSpeaking: null
}

const mutations = {
  setUserSpeaking (state, obj) {
    state.userSpeaking = obj
  },
  setStreamsCount (state, count) {
    state.streamsCount = count
  },
  incStreamCount (state) {
    state.streamsCount += 1
  },
  decStreamCount (state) {
    state.streamsCount -= 1
  },
  setConnected (state, enable) {
    state.connected = enable
    state.disconnectByControl = false
  },
  disconnectByControl (state) {
    state.connected = false
    state.disconnectByControl = true
    state.streamsCount = 0
  },
  setRoom (state, room) {
    state.room = room
  },
  setEnableAudio (state) {
    state.enableAudio = !state.enableVideo
  },
  setEnableVideo (state) {
    state.enableVideo = !state.enableVideo
  },
  setMuteAudio (state) {
    state.muteAudio = !state.muteAudio
    state.muteMicro = true
  },
  setMuteMicro (state) {
    if (state.muteMicro) {
      state.muteAudio = false
      state.muteMicro = false
      return
    }
    state.muteMicro = !state.muteMicro
  },
  setStatusConnecting (state) {
    state.status = 'connecting'
  },
  setStatusConnected (state) {
    state.status = 'connected'
  },
  setStatusDisconnected (state) {
    state.status = 'disconnected'
  }

}

const actions = {
  userIsSpeaking ({ commit }, userSpeakingObj) {
    commit('setUserSpeaking', userSpeakingObj)
  },
  setStreamsCount ({ commit }, count) {
    commit('setStreamsCount', count)
  },
  disconnectAndConnect ({ commit }, room) {
    commit('setStreamsCount', 0)
    commit('setConnected', false)
    commit('setRoom', room)
    commit('setStatusConnecting')

    setTimeout(() => {
      commit('setStreamsCount', 1)
      commit('setConnected', true)
    }, 2000)
  },
  changeToVideo ({ commit }) {
    commit('setEnableVideo')
    commit('setConnected', false)

    commit('setConnected', false)
    setTimeout(() => {
      commit('setConnected', true)
    }, 4000)
  }
}

export default {
  state,
  mutations,
  actions
}
