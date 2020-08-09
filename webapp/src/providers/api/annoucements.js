import axios from 'axios'

import { urlBase } from '../config'

export default {
  getBirthdays () {
    return axios.get(`${urlBase}/users/list/birthdays/`)
  },
  getList () {
    return axios.get(`${urlBase}/core/announcements/`)
  },
  postAnnouncement (payload) {
    return axios.post(`${urlBase}/core/announcements/`, payload)
  }
}
