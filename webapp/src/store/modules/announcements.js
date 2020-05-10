import apiClient from '../../services/api'
console.log(apiClient)
const state = {
  list: [],
  birthdays: []
}

const mutations = {
  setList(state, list) {
    state.list = list
  },
  setBirthdays(state, list) {
    state.birthdays = list
  }
}

const actions = {
  async getBirthdays({ commit }) {
    const {data} = await apiClient.announcements.getBirthdays()
    console.log(data)
    commit('setBirthdays', data)
  },
  async getList({ commit }) {
    const {data} = await apiClient.announcements.getList()
    console.log(data)
    commit('setList', data)
  },
  async postAnnouncement({ dispatch }, payload) {
    const {data} = await apiClient.announcements.postAnnouncement(payload)
    console.log(data)
    dispatch('getList')
  }
}

export default {
  state,
  mutations,
  actions
}
