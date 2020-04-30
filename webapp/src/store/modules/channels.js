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
  async getList({ commit }) {
    const {data} = await apiClient.getChannels()
    console.log(data)
    commit('setList', data)
  }
}

export default {
  state,
  mutations,
  actions
}
