
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
  },
  uploadFiles (room, payload){
    const formData = new FormData()
    for(var i = 0; i < payload.files.length; i++ ){
      let file = payload.files[i];
      formData.append('files[' + i + ']', file);
    }
    formData.append('text', payload.message)
    return axios.post(`${urlBase}/chat/room/${room}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}
