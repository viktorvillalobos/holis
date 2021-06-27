
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getTurnCredentials () {
    return axios.get(`${urlBase}/chat/get-turn-credentials/`)
  },
  getUsers () {
    return axios.get(`${urlBase}/users/`, { params: { limit: 999 } })
  },
  getRecents (search) {
    const params ={
      search: search
    }
    return axios.get(`${urlBase}/chat/recents/`,{params: params})
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
  sendMessageWithFiles (room, payload) {
    const formData = new FormData()
    payload.files.forEach(file => {
      formData.append('files', file)
    })
    formData.append('text', payload.message)
    return axios.post(`${urlBase}/chat/room/${room}/messages/new-with-attachments/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}
