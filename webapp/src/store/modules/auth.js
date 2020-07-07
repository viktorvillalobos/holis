import apiClient from "../../services/api"
import axios from 'axios'

function setDefaultHeader(token) {
    axios.defaults.headers.common['Authorization'] = `Basic ${token}`
}

const state = {
  token: null,
  company: null
}
const getters = {
    jwt: state => state.currentJWT,
}

const mutations = {
  setToken (state, token) {
    state.token = token
  },
  setCompany (state, company){
    state.company = company
  }
}

const actions = {
  async login ({state, commit}, {email, password}) {
    const { data } = await apiClient.auth.login(email, password, state.company.id)
    commit("setToken", data.token)
    localStorage.setItem('token', data.token)
    setDefaultHeader(data.token)
    document.cookie = `X-WS-Authorization=${data.token}; path=/`
    return data
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
