
import axios from 'axios'

import { urlBase } from '../config'

export default {
  list () {
    return axios.get(`${urlBase}/core/v100/areas/`)
  }
}
