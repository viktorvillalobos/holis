import axios from 'axios'

import { urlBase } from './config'

export default {
  login(username, password){
    return axios.post(`${urlBase}/token/`, {
      username,
      password
    })
  },
  refresh(refresh){
    return axios.post(`${urlBase}/token/refresh/`, {
      refresh,
    })
  },
  getAnnouncements(){
    return axios.get(`${urlBase}/announcements/`)
  }
}
