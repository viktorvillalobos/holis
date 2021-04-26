import apiClient from '../../providers/api'
import Project from '../../models/project'

const state = {
  currentScreen: 'main',
  projects: [],
  isProjectsActive: false,
  project: null,
  typeProject: 'my_projects'
}
  
const mutations = {
  setCurrentScreen(state, screen){
    state.currentScreen = screen
  },
  setProjects(state, payload) {
    state.projects = payload.map(project => new Project(project))
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
    //if(data.status == 200){
      const { dataTasks } = await apiClient.projects.addTasksProject(data.uuid, payload.tasks)
      console.log(dataTasks)
    //}
    commit('setProject', data)
  },
  async setCurrentScreen ({ commit }, screen) {
    commit('setCurrentScreen', screen)
  }
}

export default {
  state,
  mutations,
  actions
}