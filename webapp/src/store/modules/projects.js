import apiClient from '../../providers/api'

const state = {
  projects: [],
  isProjectsActive: false,
  project: null,
  typeProject: 'my_projects'
}
  
const mutations = {
    setProjects(state, payload) {
      state.projects = payload
    },
    setProject(state, payload) {
      state.project = payload
    },
    setTypeProject(state, type) {
      state.typeProject = type
    },
}

const actions = {
  async getProjects ({ commit }, type) {
    const { data } = await apiClient.projects.getProjects(type)
    console.log(data)
    commit('setProjects', data.results)
  },
  async createProject ({ commit }, payload) {
    const { data } = await apiClient.projects.createProject(payload.type, payload.data)
    console.log(data)
    commit('setProject', data)
  },
  async setTypeProject ({ commit }, type) {
    commit('setTypeProject', type)
  }
}

export default {
  state,
  mutations,
  actions
}