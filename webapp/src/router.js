import Vue from 'vue'
import Router from 'vue-router'
import Office from '@/views/office.vue'
import Login from '@/views/login.vue'

Vue.use(Router)

const router = new Router({
  // mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: '',
      component: Office
    },
    {
      path: '/login',
      name: '',
      component: Login
    }
  ]
})

// router.beforeEach((to, from, next) => {
//   console.log(to)
//   console.log(from)
//   console.log(next)
// })

export default router