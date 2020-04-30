
import axios from 'axios'

import { urlBase } from '../config'

  /* * * * * * * * * * * * * * * * * * * * *
  * We are using Django SESSION for login  *
  * but this allow to login using JWT      *
  * * * * * * * * * * * * * * * * * * *  * */

export default {
  login(username, password){
    return axios.post(`${urlBase}/token/`, {
      username,
      password
    })
  },
  refresh(refresh){
    return axios.post(`${urlBase}/token/refresh/`, {
      refresh,
    })
  },
}
