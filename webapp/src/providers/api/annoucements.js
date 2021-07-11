import axios from 'axios'

import { urlBase } from '../config'

export default {
  getBirthdays () {
    return axios.get(`${urlBase}/users/v100/list/birthdays/`)
  },
  getList () {
    return axios.get(`${urlBase}/core/v100/announcements/`)
  },
  postAnnouncement (payload) {
    return axios.post(`${urlBase}/core/v100/announcements/`, payload)
  }
}
