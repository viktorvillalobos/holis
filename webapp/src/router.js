import Vue from 'vue'
import Router from 'vue-router'
import AppContainer from '@/components/AppContainer.vue'
import Office from '@/views/office.vue'
import Reports from '@/views/reports.vue'

import Config from '@/views/config.vue'
import UserConfig from '@/components/Config/UserConfig'
import VoiceAndVideo from '@/components/Config/VoiceAndVideo'
import Notifications from '@/components/Config/Notifications'
import Invitations from '@/components/Config/Invitations'
import UsersRole from '@/components/Config/UsersRole'

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
          component: Config,
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
            },
            {
              path: '/invitations',
              name: 'invitations-config',
              component: Invitations
            },
            {
              path: '/users-role',
              name: 'users-role-config',
              component: UsersRole
            }
          ]
        }
      ]
    }
  ]
})

export default router
