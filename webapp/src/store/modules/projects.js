import apiClient from '../../providers/api'

const state = {
    isProjectsActive: false
}
  
const mutations = {
    setProjectsActive (state) {
      state.isNotificationsActive = !state.isNotificationsActive
    }
}

const actions = {
  async getProjects ({ commit }, type) {
    console.log("Entre aqui")
    const { data } = await apiClient.projects.getProjects(type)
    commit('setProjects', data.results)
  }
}

export default {
  state,
  mutations,
  actions
}