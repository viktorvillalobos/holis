import apiClient from '../../services/api'
const state = {
  users: [],
  channels: []
}

const mutations = {
  setUsers(state, list) {
    state.users = list
  },
  setChannels(state, list) {
    state.channels = list
  }
}

const actions = {
  async getUsers({ commit }) {
    const {data} = await apiClient.chat.getUsers()
    console.log(data)
    commit('setUsers', data.results)
  },
  async getChannels({ commit }) {
    const {data} = await apiClient.chat.getChannels()
    console.log(data)
    commit('setChannels', data)
  }
}

export default {
  state,
  mutations,
  actions
}
