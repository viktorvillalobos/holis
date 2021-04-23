
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getTypeNumber(type){
    var typeNumber = 1
    switch(type) {
      case 'my_projects':
        typeNumber = 1
        break
      case 'my_team':
        typeNumber = 2
        break
      default:
        typeNumber = 3
        break
    }
    return typeNumber
  },
  getProjects(type) {
    return axios.get(`${urlBase}/projects/kind/${this.getTypeNumber(type)}`)
  },
  createProject (type, payload) {
    console.log("Type",type)
    console.log("Payload",payload)
    return axios.post(`${urlBase}/projects/kind/${this.getTypeNumber(type)}`, payload)
  }
}
