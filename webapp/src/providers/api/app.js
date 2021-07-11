
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getReleases () {
    return axios.get(`${urlBase}/core/v100/changelogs/`, { params: { limit: 20 } })
  },
  getNotifications () {
    return axios.get(`${urlBase}/users/v100/notifications/`, { params: { limit: 999 } })
  },
  setStatus (statusId) {
    return axios.post(`${urlBase}/users/v100/set-status/`, { status_id: statusId })
  },
  getMe () {
    return axios.get(`${urlBase}/users/v100/profile/`)
  },
  getUser (id) {
    return axios(`${urlBase}/users/v100/${id}/`)
  },
  editUser (payload) {
    return axios.patch(`${urlBase}/users/v100/profile/edit/`, payload)
  },
  setProfilePicture (file) {
    console.assert(file instanceof File, 'You must provide a File instance')
    const formData = new FormData()
    formData.append('avatar', file)
    return axios.post(`${urlBase}/users/v100/me/upload-avatar/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}
