
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getCredentials () {
    return axios.get(`${urlBase}/get-chat-credentials/`)
  },
  getTurnCredentials () {
    return axios.get(`${urlBase}/get-turn-credentials/`)
  },
  getUsers () {
    return axios.get(`${urlBase}/users/`, { params: { limit: 999 } })
  }
}
