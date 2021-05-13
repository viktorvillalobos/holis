import apiClient from '../../providers/api'
const state = {
  user: null,
  isAsideLeftActive: false,
  isAsideRightActive: false,
  isBoardActive: false,
  isReleasesActive: false,
  isMicroActive: false,
  isVideoActive: false,
  isSoundActive: true,
  releases: [],
  notifications: [],
  alert: {
    active: false,
    text: 'Are you sure you wanna get out of this voice channel?',
    title: 'Wait!',
    icon: 'grin-beam-sweat'
  }
}

const mutations = {
  setUser (state, user) {
    state.user = user
  },
  setAsideLeftActive (state) {
    state.isAsideLeftActive = !state.isAsideLeftActive
  },
  setAsideRightActive (state, status) {
    status ? state.isAsideRightActive = true : state.isAsideRightActive = !state.isAsideRightActive
  },
  setBoardActive (state) {
    state.isBoardActive = !state.isBoardActive
  },
  setReleasesActive (state) {
    state.isReleasesActive = !state.isReleasesActive
  },
  setMicroActive (state) {
    state.isMicroActive = !state.isMicroActive
  },
  setVideoActive (state) {
    state.isVideoActive = !state.isVideoActive
  },
  setSoundActive (state) {
    state.isSoundActive = !state.isSoundActive
  },
  setReleases (state, payload) {
    state.releases = payload
  },
  setAlert (state, payload) {
    state.alert = payload
  }
}

const actions = {
  async getReleases ({ commit }) {
    const { data } = await apiClient.app.getReleases()
    commit('setReleases', data.results)
  },
  async getMe ({ commit }) {
    const { data } = await apiClient.app.getMe()
    commit('setUser', data)
  },
  async getUser ({ commit }, id) {
    const { data } = await apiClient.app.getUser(id)
    commit('setUser', data)
  },
  async editUser ({ commit }, payload) {
    const { data } = await apiClient.app.editUser(payload)

    console.log('Saving User Data')
    console.log(data)
    commit('setUser', data)
  },
  async setProfilePicture ({ commit }, file) {
    const { data } = await apiClient.app.setProfilePicture(file)

    console.log('setProfilePicture')
    console.log(data)
  }
}

export default {
  state,
  mutations,
  actions
}
