import apiClient from '../../providers/api'
import notificationServices from '../../services/notification'

const socketNotificationsUrl =
  process.env.NODE_ENV === 'production'
    ? `wss://${location.hostname}:${location.port}/ws/notifications/`
    : `ws://${location.hostname}:${location.port}/ws/notifications/`

const state = {
  notifications: [],
  isNotificationsActive: false,
  notification: {
    show: false,
    text: 'This is a demo notification',
    type: 'default'
  }
}

const mutations = {
  setNotificationsActive (state) {
    state.isNotificationsActive = !state.isNotificationsActive
  },
  setNotifications (state, payload) {
    state.notifications = payload
  },
  setActiveNotification (state, notification) {
    const data = {
      show: true,
      text: notification.message,
      type: notification.ntype
    }
    state.notification = data
  },
  closeActiveNotification (state) {
    state.notification.show = false
  }
}

const actions = {
  async connectNotificationsChannel ({ commit, state, getters, dispatch }, vm) {
    const callback = notification => dispatch('onNotification', notification.data)

    notificationServices.setSocketService({
      url: socketNotificationsUrl,
      callback
    })
  },
  async getNotifications ({ commit }) {
    const { data } = await apiClient.app.getNotifications()
    commit('setNotifications', data.results)
  },
  onNotification ({ commit }, notification) {
    notification = JSON.parse(notification)
    console.log(notification)
    if (notification.type === 'notification') commit('setActiveNotification', notification)
  }
}

export default {
  state,
  mutations,
  actions
}
