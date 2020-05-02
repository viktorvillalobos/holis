import apiClient from "../../services/api"

const state = {
  currentArea: null,
  list: [],
  changeState: null,
}

const getters = {
  currentState (state) {
    return state.currentArea ? state.currentArea.state : []
  }
}

const mutations = {
  setCurrent(state) {
    // TODO: Selectable area
    if (state.list) {
      state.currentArea = state.list[0]
    }
  },
  setAreas(state, areas) {
    state.list= areas
  },
}

const actions = {
  async getAreas({ commit }) {
    const { data } = await apiClient.areas.list()
    commit('setAreas', data.results)
    commit('setCurrent')
  }
}

export default {
  state,
  getters,
  mutations,
  actions,
}