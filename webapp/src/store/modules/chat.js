import apiClient from '../../services/api'
const state = {
  users: []
}

const mutations = {
  setUsers(state, list) {
    state.users = list
  }
}

const actions = {
  async getUsers({ commit }) {
    const {data} = await apiClient.chat.getUsers()
    console.log(data)
    commit('setUsers', data.results)
  }
}

export default {
  state,
  mutations,
  actions
}
