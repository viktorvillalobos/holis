import apiClient from "../../services/api"
import axios from 'axios'

function setDefaultHeader(jwt) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${jwt}`
}

const state = {
  currentJWT: null,
  refresh: null,
  company: null
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
  },
  setCompany (state, company){
    state.company = company
  }
}

const actions = {
  login ({state}, {email, password}) {
    const data = apiClient.auth.login(email, password, state.company.id)
    // setDefaultHeader(data.access)
    // commit("setJWT", data.access)
    // commit("setRefresh", data.refresh)
    return data
  },
  refresh ({commit}, {username, password}) {
    const {data} = apiClient.login(username, password)
    setDefaultHeader(data.access)
    commit("setJWT", data.access)
  },
  async checkCompany ({commit}, {companyName}){
    try{
      const {data} = await apiClient.auth.checkCompany(companyName)
      console.log('company', data)
      commit("setCompany", data)
    }catch(error){
      console.error(error)
    }
  },
}

export default {
  state,
  getters,
  mutations,
  actions
}
