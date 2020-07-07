import Vue from 'vue'
import Router from 'vue-router'
import AppContainer from '@/components/AppContainer.vue'
import Workspace from '@/components/Auth/Workspace.vue'
import WhoYou from '@/components/Auth/WhoYou.vue'
import Invite from '@/components/Auth/Invite.vue'
import Company from '@/components/Auth/Company.vue'
import SignIn from '@/components/Auth/SignIn.vue'
import Office from '@/views/office.vue'
import Reports from '@/views/reports.vue'
import Auth from '@/views/auth.vue'

Vue.use(Router)
const ifNotAuthenticated = (to, from, next) => {
  if (!localStorage.getItem('token')) {
        next()
        return
      
  }
    next('/')
  
}

const ifAuthenticated = (to, from, next) => {
  if (localStorage.getItem('token')) {
        next()
        return
      
  }
    next('/auth/s/')
  
}

const router = new Router({
  // mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: '',
      component: AppContainer,
      beforeEnter: ifAuthenticated,
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
      beforeEnter: ifNotAuthenticated,
      children: [
        {
          path: 's/',
          name: 'workspace',
          component: Workspace
        },
        {
          path: 's/:workspaceName',
          name: 'sign-in',
          component: SignIn
        },
        {
          path: 'c/',
          name: 'create-workspace',
          component: WhoYou
        },
        {
          path: 'c/company',
          name: 'create-company',
          component: Company
        },
        {
          path: 'c/invite',
          name: 'create-invitations',
          component: Invite
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
