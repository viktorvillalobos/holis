
import axios from 'axios'

import { urlBase } from '../config'

export default {
  activeNotifications (token) {
    const form = {
        "registration_id": token,
        "active": true,
        "type": "web"
    }
    return axios.post(`${urlBase}/users/v100/devices/`, form)
  },
}
