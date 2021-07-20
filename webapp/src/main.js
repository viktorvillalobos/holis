import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueNativeSock from 'vue-native-websocket'
import AxiosDjango from '@/plugins/AxiosDjango'
import VueApexCharts from 'vue-apexcharts'
import VueLodash from 'vue-lodash'
import lodash from 'lodash'
import vuescroll from 'vuescroll'

import { library } from '@fortawesome/fontawesome-svg-core'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import firebaseMessaging from '../boots/firebase'

Vue.prototype.$messaging = firebaseMessaging
Vue.prototype.$messaging.usePublicVapidKey('BN228XTdBTOuaK-qP_6SaMzGxIfgRVHWC9u4z4zVIyQi1ewgjGOKq8n8P781YD6J-jrFbSO62svnmC2K5NVdUos')

import '@/plugins/mask.js'

const moment = require('moment')
require('moment/locale/es')

Vue.use(require('vue-moment'), {
  moment
})

Vue.use(VueLodash, { name: 'piso', lodash: lodash })

Vue.component('apexchart', VueApexCharts)

library.add(far)
library.add(fas)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(AxiosDjango)

const socket = process.env.NODE_ENV === 'production'
  ? `wss://${location.hostname}:${location.port}/ws/grid/`
  : `ws://${location.hostname}:${location.port}/ws/grid/`

Vue.use(VueNativeSock, socket, {
  connectManually: true
})

Vue.use(vuescroll, {
  ops: {
    bar: {
      background: '#5d6de8'
    }
  }
})

const app = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

store.$app = app
