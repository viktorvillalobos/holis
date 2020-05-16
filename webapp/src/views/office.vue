<template>
  <div class="connect-office-view">
    <hexagonal-grid :size="38" />
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
  </div>
</template>
<script>
import {mapState} from 'vuex'
import HexagonalGrid from "@/components/HexagonalGrid"
import WebRTC from "@/components/WebRtc"

export default {
  name: "Office",
  components: {
    HexagonalGrid,
    webrtc: WebRTC
  },
  data () {
    return {
      connect: false
    }
  },
  computed: {
    ...mapState({
      room: state => state.webrtc.room,
      connected: state => state.webrtc.connected,
      muteAudio: state => state.webrtc.muteAudio,
      muteMicro: state => state.webrtc.muteMicro,
      enableAudio: state => state.webrtc.enableAudio,
      enableVideo: state => state.webrtc.enableVideo,
      float : state => state.app.isAsideRightActive,
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
      if (value) this.$refs.webrtc.join();
      else this.$refs.webrtc.leave();
    }
  }
};
</script>
<style lang="scss">
.connect-office-view {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1;
}

.video-list {
  position: fixed;
  right: 70px;
  bottom: 18px;
  width: 220px;
  border-radius: 10px;
  transition: $aside-transition;

  &.aside-expanded {
    right: 400px;
  }
}
</style>
