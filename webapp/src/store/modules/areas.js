import apiClient from "../../services/api"

const state = {
  currentArea: null,
  areas: [],
}

const getters = {
  currentState (state) {
    return state.currentArea ? state.currentArea.staate : []
  }
}

const mutations = {
  setCurrentArea(state, area) {
    state.currentArea = area
  },
  setAreas(state, areas) {
    state.areas = areas
  },
}

const actions = {
  async getAreas({ commit }) {
    const { data } = await apiClient.areas.list()
    commit('setAreas', data)
  }
}

export default {
  state,
  getters,
  mutations,
  actions,
}
