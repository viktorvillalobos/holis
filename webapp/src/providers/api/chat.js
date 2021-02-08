
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getTurnCredentials () {
    return axios.get(`${urlBase}/chat/get-turn-credentials/`)
  },
  getUsers () {
    return axios.get(`${urlBase}/users/`, { params: { limit: 999 } })
  },
  getRecents () {
    return axios.get(`${urlBase}/chat/recents/`)
  },
  getRoomByUserID (to) {
    return axios.post(`${urlBase}/chat/get-or-create-room/`, { to })
  },
  getMessages (room) {
    return axios.get(`${urlBase}/chat/room/${room}/messages/`)
  },
  getMessagesFromUrl (url) {
    return axios.get(url)
  }
}
