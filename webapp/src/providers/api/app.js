
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getReleases () {
    return axios.get(`${urlBase}/core/changelogs/`, { params: { limit: 20 } })
  },
  getNotifications () {
    return axios.get(`${urlBase}/users/notifications/`, { params: { limit: 999 } })
  },
  setStatus (statusId) {
    return axios.post(`${urlBase}/users/set-status/`, { status_id: statusId })
  },
  getMe () {
    return axios.get(`${urlBase}/users/profile/`)
  },
  getUser (id) {
    return axios(`${urlBase}/users/${id}/`)
  },
  editUser (payload) {
    return axios.patch(`${urlBase}/users/profile/edit/`, payload)
  }
}
