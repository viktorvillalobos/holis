import axios from 'axios'

import { urlBase } from '../config'

export default {
  getBirthdays () {
    return axios.get(`${urlBase}/users/birthdays/`)
  },
  getList () {
    return axios.get(`${urlBase}/announcements/`)
  },
  postAnnouncement (payload) {
    return axios.post(`${urlBase}/announcements/`, payload)
  }
}
