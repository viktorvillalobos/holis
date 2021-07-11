
import axios from 'axios'

import { urlBase } from '../config'

/* * * * * * * * * * * * * * * * * * * * *
  * We are using Django SESSION for login  *
  * but this allow to login using JWT      *
  * * * * * * * * * * * * * * * * * * *  * */

export default {
  login (email, password, company) {
    return axios.post(`${urlBase}/v100/login/`, {
      email,
      password,
      company
    })
  },

  checkCompany (companyName) {
    return axios.get(`${urlBase}/check-company/${companyName}`)
  }
}
