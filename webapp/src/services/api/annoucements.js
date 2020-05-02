import axios from 'axios'

import { urlBase } from '../config'

export default {
  getList(){
    return axios.get(`${urlBase}/announcements/`)
  },
  postAnnouncement (payload) {
    return axios.post(`${urlBase}/announcements/`, payload)
  }
}
