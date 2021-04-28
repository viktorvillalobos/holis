import apiClient from '../../providers/api'
import Project from '../../models/project'

const state = {
  currentScreen: {
    'screen' : 'main',
    'data' : null
  },
  projects: [],
  isProjectsActive: false,
  project: null,
  typeProject: 'my_projects',
  tasks:[]
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
  setTasksProject(state, payload) {
    state.tasks = payload
  },
}

const actions = {
  async getProjects ({ commit }, type) {
    const { data } = await apiClient.projects.getProjects(type)
    console.log(data)
    commit('setProjects', data.results)
  },
  async createProject ({ commit }, payload) {
    const { data } = await apiClient.projects.createProject(payload.typeProject, payload.data)
    console.log(data)
    //if(data.status == 200){
      const { dataTasks } = await apiClient.projects.addTasksProject(data.uuid, payload.tasks)
      console.log(dataTasks)
    //}
    commit('setProject', data)
  },
  async setCurrentScreen ({ commit }, screen) {
    commit('setCurrentScreen', screen)
  },
  async getTasksProject ({ commit }, uuid) {
    const { data } = await apiClient.projects.getTasksProject(uuid)
    console.log(data)
    data.results.forEach((element,index) => {
      data.results[index].titleEdit = false
      data.results[index].contentEdit = false
    });
    commit('setTasksProject', data.results)
  },
}

export default {
  state,
  mutations,
  actions
}