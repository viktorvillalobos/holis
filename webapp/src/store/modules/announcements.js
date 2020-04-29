import apiClient from '../../services/apiClient.js'
const state = {
  list: []
}

const mutations = {
  setList(state, list) {
    state.list = list
  }
}

const actions = {
  getList({ commit }) {
    const {data} = apiClient.getAnnouncements()
    commit('setList', data)
  }
}

export default {
  state,
  mutations,
  actions
}
