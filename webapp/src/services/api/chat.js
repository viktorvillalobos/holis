
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getCredentials () {
    return axios.get(`${urlBase}/chat/get-chat-credentials/`)
  },
  getTurnCredentials () {
    return axios.get(`${urlBase}/chat/get-turn-credentials/`)
  },
  getUsers () {
    return axios.get(`${urlBase}/users/list/`, { params: { limit: 999 } })
  },
  getRecents () {
    return axios.get(`${urlBase}/chat/recents/`)
  },
}
