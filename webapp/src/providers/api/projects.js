
import axios from 'axios'

import { urlBase } from '../config'

export default {
  getTypeNumber(type){
    var typeNumber = 1
    switch(type) {
      case 'my_projects':
        typeNumber = 3
        break
      case 'my_team':
        typeNumber = 2
        break
      default:
        typeNumber = 1
        break
    }
    return typeNumber
  },
  getProjects(type) {
    console.log(`${urlBase}/projects/kind/${this.getTypeNumber(type)}`)
    return axios.get(`${urlBase}/projects/kind/${this.getTypeNumber(type)}`)
  },
  createProject (type, payload) {
    console.log("Type",type)
    console.log("Payload",payload)
    console.log(`${urlBase}/projects/kind/${this.getTypeNumber(type)}`)
    return axios.post(`${urlBase}/projects/kind/${this.getTypeNumber(type)}`, payload)
  },
  addTasksProject (project_uuid, payload) {
    console.log("project_uuid",project_uuid)
    console.log("Payload",payload)
    return axios.post(`${urlBase}/projects/${project_uuid}/tasks`, payload)
  },
  getTasksProject (project_uuid) {
    console.log("project_uuid",project_uuid)
    console.log("url",`${urlBase}/projects/${project_uuid}/tasks`)
    return axios.get(`${urlBase}/projects/${project_uuid}/tasks`)
  }
}
