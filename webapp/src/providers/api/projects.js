
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getProjects(type) {
    return axios.get(`${urlBase}/projects/kind/${type}/`)
  }
}
