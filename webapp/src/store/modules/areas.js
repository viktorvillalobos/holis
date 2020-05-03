import apiClient from "../../services/api"

const state = {
  currentArea: null, // Initial state called from rest
  list: [],
  changeState: null, // Message of a state change
}

const getters = {
  currentState (state) {
    return state.currentArea ? state.currentArea.state : []
  },
  occupedPoints (state) {
    const areaState =  state.currentArea ? state.currentArea.state : []
    return areaState 
      ? areaState.map((item) => {
        return {x: item.x, y: item.y}
      }) 
      : []
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
  setOccupedStateChange(state, change) {
    /* When a new position is received we neeed to updeda
      * the currentArea.state        
      * we need to find the last point to release
      * and then occuped the new
      * */
    state.currentArea.state =  change
  }
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
