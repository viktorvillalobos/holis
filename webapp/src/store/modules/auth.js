import apiClient from "../../services/apiClient"
import axios from 'axios'

function setDefaultHeader(jwt) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${jwt}`
}

const state = {
  currentJWT: null,
  refresh: null
}
const getters = {
    jwt: state => state.currentJWT,
    jwtData: (state, getters) => state.currentJWT ? JSON.parse(atob(getters.jwt.split('.')[1])) : null,
    jwtSubject: (state, getters) => getters.jwtData ? getters.jwtData.sub : null,
    jwtIssuer: (state, getters) => getters.jwtData ? getters.jwtData.iss : null
}

const mutations = {
  setJWT (state, jwt) {
    state.currentJWT = jwt
  },
  setRefresh (state, token) {
    state.refresh = token
  }
}

const actions = {
  login ({commit}, {username, password}) {
    const {data} = apiClient.login(username, password)
    setDefaultHeader(data.access)
    commit("setJWT", data.access)
    commit("setRefresh", data.refresh)
  },
  refresh ({commit}, {username, password}) {
    const {data} = apiClient.login(username, password)
    setDefaultHeader(data.access)
    commit("setJWT", data.access)
  },
}

export default {
  state,
  getters,
  mutations,
  actions
}
