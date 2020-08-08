
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getTurnCredentials () {
    return axios.get(`${urlBase}/chat/get-turn-credentials/`)
  },
  getUsers () {
    return axios.get(`${urlBase}/users/list/`, { params: { limit: 999 } })
  },
  getRecents () {
    return axios.get(`${urlBase}/chat/recents/`)
  },
  getMessages (room) {
    return axios.get(`${urlBase}/chat/room/${room}/messages/`, { params: { limit: 20 } })
  }
}
