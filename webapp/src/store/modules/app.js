import apiClient from '../../services/api'
const state = {
  user: null,
  isAsideLeftActive: false,
  isAsideRightActive: false,
  isBoardActive: false,
  isReleasesActive: false,
  isNotificationsActive: false,
  notification: {
    show: false,
    text: 'This is a demo notification'
  },
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
  setNotificationsActive (state) {
    state.isNotificationsActive = !state.isNotificationsActive
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
  setNotifications (state, payload) {
    state.notifications = payload
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
  async getNotifications ({ commit }) {
    const { data } = await apiClient.app.getNotifications()
    commit('setNotifications', data.results)
  },
  async getMe ({ commit }) {
    const { data } = await apiClient.app.getMe()
    commit('setUser', data)
  }
}

export default {
  state,
  mutations,
  actions
}
