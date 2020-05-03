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

    const areaState = [...state.currentArea.state]
    console.log('CurrentArea')
    console.log(areaState)
    const filtered = areaState.filter(x => x.id !== change.user.id)
    console.log('Filtered')
    console.log(filtered)
    const result = [...filtered, change]
    console.log('Result')
    console.log(result)
    state.currentArea.state =  result
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
