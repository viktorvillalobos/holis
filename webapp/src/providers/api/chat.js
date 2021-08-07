
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getTurnCredentials () {
    return axios.get(`${urlBase}/chat/v100/get-turn-credentials/`)
  },
  getUsers (search) {
    const params ={
      name: search,
      limit: 999
    }
    return axios.get(`${urlBase}/users/v100/`, { params: params })
  },
  getRecents (search) {
    const params = {
      search: search
    }
    return axios.get(`${urlBase}/chat/v100/room/recents/`,{params: params})
  },
  getRoomByUserID (to) {
    return axios.post(`${urlBase}/chat/v100/get-or-create-room/`, {
      to: [to]
    })
  },
  getMessages (room) {
    return axios.get(`${urlBase}/chat/v100/room/${room}/messages/`)
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
    return axios.post(`${urlBase}/chat/v100/room/${room}/messages/new-with-attachments/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}
