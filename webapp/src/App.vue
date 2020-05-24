<template>
  <div id="app">
    <webrtc
      :class="{'aside-expanded' : !float}"
      ref="webrtc"
      width="100%"
      :roomId="room"
      :enableAudio="enableAudio"
      :enableVideo="enableVideo"
      v-on:joined-room="logEvent"
      v-on:left-room="logEvent"
      v-on:open-room="logEvent"
      v-on:share-started="logEvent"
      v-on:share-stopped="logEvent"
      @error="onError"
    />

    <router-view></router-view>
  </div>
</template>

<script>

window.onbeforeunload = function(e) {
    e = e || window.event;

    // For IE and Firefox prior to version 4
   if (e) {
        e.returnValue = 'Sure?';
   }
   return 'Dialog text here.';
};

import { mapState } from 'vuex'
import WebRTC from "@/components/WebRtc"

export default {
  name: "App",
  components: {
    webrtc: WebRTC
  },
  computed: {
    ...mapState({
      room: state => state.webrtc.room,
      connected: state => state.webrtc.connected,
      muteAudio: state => state.webrtc.muteAudio,
      muteMicro: state => state.webrtc.muteMicro,
      enableAudio: state => state.webrtc.enableAudio,
      enableVideo: state => state.webrtc.enableVideo,
    })
  },
  methods: {
    logEvent(event) {
      console.log("Event : ", event);
    },
    onError(error, stream) {
      console.log("On Error Event", error, stream);
    },
    onCapture() {
      this.img = this.$refs.webrtc.capture();
    },
    onJoin() {
      console.log("Join to the connection");
    },
    onLeave() {
      this.$refs.webrtc.leave();
    },
    onShareScreen() {
      this.img = this.$refs.webrtc.shareScreen();
    }
  },
  watch: {
    connected(value) {
      console.log('Changing Connected Watcher in Office')
      if (value) this.$refs.webrtc.join();
      else this.$refs.webrtc.leave();
    }
  }
};
</script>

<style lang="scss">
</style>
