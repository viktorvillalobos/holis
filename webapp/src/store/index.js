import Vue from 'vue'
import Vuex from 'vuex'
import app from './modules/app'
import auth from './modules/auth'
import announcements from './modules/announcements'
import areas from './modules/areas'
import chat from './modules/chat'
import webrtc from './modules/webrtc'

Vue.use(Vuex)

const store = new Vuex.Store({
  strict: true, // process.env.NODE_ENV !== 'production',
  modules: {
    app,
    auth,
    announcements,
    areas,
    chat,
    webrtc
  },
  state: {
    socket: {
      isConnected: false,
      message: '',
      reconnectError: false,
    }
  },
  mutations:{
    SOCKET_ONOPEN (state, is_active)  {
      console.log('Socket ONOPEN')
      state.socket.isConnected = is_active
    },
    /* eslint-disable-next-line */
    SOCKET_ONCLOSE (state, event)  {
      state.socket.isConnected = false
    },
    SOCKET_ONERROR (state, event)  {
      console.error(state, event)
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE (state, message)  {
      console.log('Socket ONMESSAGE')
      console.log(message)
      state.socket.message = message

      switch (message.type){
        case 'notification':
          state.app.notification.show = true
          state.app.notification.text = message.message
        break
        case 'me.data':
          state.app.user = message.user
        break
        case 'grid.position':
          // Change the received message
          state.areas.changeState = message
        break
        case 'grid.disconnect':
          state.areas.deleteFromState = message
        break
      }
    },
    // mutations for reconnect methods
    SOCKET_RECONNECT(state, count) {
      console.info(state, count)
    },
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true;
    },
  },
  actions: {
    setSocketState({commit}, is_active) {
      commit('SOCKET_ONOPEN', is_active)
    }
  }
})

export default store
