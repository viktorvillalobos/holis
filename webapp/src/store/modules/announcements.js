import apiClient from '../../services/api'
console.log(apiClient)
const state = {
  list: []
}

const mutations = {
  setList(state, list) {
    state.list = list
  }
}

const actions = {
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
