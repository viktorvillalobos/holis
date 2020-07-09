
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getReleases () {
    return axios.get(`${urlBase}/changelogs/`, { params: { limit: 20 } })
  },
  getNotifications () {
    return axios.get(`${urlBase}/notifications/`, { params: { limit: 999 } })
  }
}
