
import axios from 'axios'

import { urlBase } from '../config'

export default {
    getUsers() {
        return axios.get(`${urlBase}/users/`, { params: { limit: 999 } })
    },
    getChannels() {
        return axios.get(`${urlBase}/channels/`, { params: { limit: 999 } })
    },
}
