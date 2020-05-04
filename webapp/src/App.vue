<template>
  <div id="app">
      <vue-webrtc ref="webrtc"
          v-show="false"
          width="100%"
          :roomId="adslab"
          :enableAudio="true"
          :enableVideo="false"
          v-on:joined-room="logEvent"
          v-on:left-room="logEvent"
          v-on:open-room="logEvent"
          v-on:share-started="logEvent"
          v-on:share-stopped="logEvent"
          @error="onError" />
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  created() {
    this.$store.dispatch("getList")
  },
  mounted() {
    this.$refs.webrtc.join()
  },
  methods: {
   logEvent(event) {
       console.log('Event : ', event);
    },
    onCapture() {
      this.img = this.$refs.webrtc.capture();
    },
    onJoin() {
      this.$refs.webrtc.join();
    },
    onLeave() {
      this.$refs.webrtc.leave();
    },
    onShareScreen() {
      this.img = this.$refs.webrtc.shareScreen();
    },

  }
};
</script>

<style lang="scss">
</style>
