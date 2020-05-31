import Vue from 'vue'
import Router from 'vue-router'
import AppContainer from '@/components/AppContainer.vue'
import Workspace from '@/components/Auth/Workspace.vue'
import SignIn from '@/components/Auth/SignIn.vue'
import Office from '@/views/office.vue'
import Reports from '@/views/reports.vue'
import Auth from '@/views/auth.vue'

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
        }
      ]
    },
    {
      path: '/auth/',
      name: '',
      component: Auth,
      children: [
        {
          path: '',
          name: 'workspace',
          component: Workspace
        },
        {
          path: ':workspaceName',
          name: 'sign-in',
          component: SignIn
        }
      ]
    }
  ]
})

// router.beforeEach((to, from, next) => {
//   console.log(to)
//   console.log(from)
//   console.log(next)
// })

export default router
