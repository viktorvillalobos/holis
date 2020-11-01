<template>
  <div id="app">
    <webrtc
      :class="{'aside-expanded' : !float}"
      ref="webrtc"
      width="100%"
      :roomId="room"
      :enableAudio="enableAudio"
      :enableVideo="enableVideo"
      v-on:joined-room="joinedRoom"
      v-on:left-room="leftRoom"
      v-on:open-room="logEvent"
      v-on:share-started="logEvent"
      v-on:share-stopped="logEvent"
      @error="onError"
    />

    <router-view></router-view>
  </div>
</template>

<script>

import AOS from 'aos'
import 'aos/dist/aos.css'
import { mapState } from 'vuex'
import WebRTC from '@/components/WebRtc'

export default {
  name: 'App',
  components: {
    webrtc: WebRTC
  },
  created () {
    this.$store.dispatch('getMe')
    AOS.init()
  },
  computed: {
    ...mapState({
      room: state => state.webrtc.room,
      muteAudio: state => state.webrtc.muteAudio,
      muteMicro: state => state.webrtc.muteMicro,
      enableAudio: state => state.webrtc.enableAudio,
      enableVideo: state => state.webrtc.enableVideo,
      float: state => state.app.isAsideRightActive
    })
  },
  methods: {
    logEvent (event) {
      console.log('Event : ', event)
    },
    onError (error, stream) {
      console.log('On Error Event', error, stream)
    },
    onCapture () {
      this.img = this.$refs.webrtc.capture()
    },
    onJoin () {
      console.log('Join to the connection')
    },
    onLeave () {
      this.$refs.webrtc.leave()
    },
    onShareScreen () {
      this.img = this.$refs.webrtc.shareScreen()
    },
    joinedRoom ({ isLocalUser }) {
      console.log('An user is joined to room')
      if (!isLocalUser) {
        const audio = new Audio('/static/sounds/in.m4a')
        audio.play()
      }
    },
    leftRoom ({ isLocalUser }) {
      console.log('An user left the room')
      if (!isLocalUser) {
        console.log('play left audio')
        const audio = new Audio('/static/sounds/out.m4a')
        audio.play()
      }
    }
  }
}
</script>

<style lang="scss">
</style>
