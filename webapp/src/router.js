import Vue from 'vue'
import Router from 'vue-router'
import AppContainer from '@/components/AppContainer.vue'
import Office from '@/views/office.vue'
import Reports from '@/views/reports.vue'

import config from '@/views/config.vue'
import UserConfig from '@/components/config/UserConfig'
import VoiceAndVideo from '@/components/config/VoiceAndVideo'
import Notifications from '@/components/config/Notifications'

Vue.use(Router)

const router = new Router({
  // mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: '',
      component: AppContainer,
      children: [
        {
          path: '',
          name: 'office',
          component: Office
        },
        {
          path: 'reports',
          name: 'reports',
          component: Reports
        },
        {
          path: 'config',
          name: 'config',
          component: config,
          children: [
            {
              path: '',
              name: 'user-config',
              component: UserConfig
            },
            {
              path: '/voice-and-video',
              name: 'voice-and-video-config',
              component: VoiceAndVideo
            },
            {
              path: '/notifications',
              name: 'notifications-config',
              component: Notifications
            }
          ]
        }
      ]
    }
  ]
})

export default router
