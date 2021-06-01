import apiClient from '../../providers/api'
import Project from '../../models/project'

const state = {
  currentScreen: {
    screen: 'main',
    data: null
  },
  projects: [],
  isProjectsActive: false,
  project: null,
  typeProject: 'my_projects',
  tasks: []
}

const mutations = {
  setCurrentScreen (state, screen) {
    state.currentScreen = screen
  },
  setProjects (state, payload) {
    state.projects = payload.map(project => new Project(project))
  },
  setProject (state, payload) {
    state.project = payload
  },
  setTypeProject (state, type) {
    state.typeProject = type
  },
  setTasksProject (state, payload) {
    state.tasks = payload
  }
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
    // if(data.status == 200){
    const { dataTasks } = await apiClient.projects.addTasksProject(data.uuid, payload.tasks)
    console.log(dataTasks)
    // }
    commit('setProject', data)
  },
  async addTaskProject ({ commit, dispatch }, payload) {
    const { dataTasks } = await apiClient.projects.addTasksProject(payload.project_uuid, payload.tasks)
    console.log(dataTasks)
    dispatch('getTasksProject', payload.project_uuid)
  },
  async setCurrentScreen ({ commit }, screen) {
    commit('setCurrentScreen', screen)
  },
  async getTasksProject ({ commit }, uuid) {
    const { data } = await apiClient.projects.getTasksProject(uuid)
    console.log(data)
    data.results.forEach((element, index) => {
      data.results[index].titleEdit = false
      data.results[index].contentEdit = false
      data.results[index].dropdownActive = false
    })
    commit('setTasksProject', data.results)
  },
  async updateTask ({ commit }, payload) {
    const { data } = await apiClient.projects.updateTask(payload.uuid, payload.task, payload.data)
    console.log('Update Result ', data)
  },
  async deleteTask ({ commit, dispatch }, payload) {
    const { data } = await apiClient.projects.deleteTask(payload.project_uuid, payload.task)
    console.log(data)
    dispatch('getTasksProject', payload.project_uuid)
  },
  async moveTask ({ commit, dispatch }, payload) {
    const { data } = await apiClient.projects.moveTask(payload.project_uuid, payload.task, payload.index)
    console.log(data)
  }
}

export default {
  state,
  mutations,
  actions
}
