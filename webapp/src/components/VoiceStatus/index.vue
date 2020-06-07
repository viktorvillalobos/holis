<template>
  <div class="connect-area-voice">

    <div class="connect-area-voice-status">
      <font-awesome-icon :color="icon.color" :icon="icon.icon" class="status-icon"/> 
      <div class="connect-area-voice-status-text">
          <p> {{ translateStatus }}</p>
          <span>{{ streams.length }} members</span>
      </div>
    </div>

    <div @click="disconnect" class="connect-area-voice-disconnect">
      <font-awesome-icon v-if="connected" icon="phone-slash" />
      <font-awesome-icon v-else icon="phone-slash" disabled color="grey"/>
    </div>
  </div>
</template>
<script>
import { mapState } from 'vuex'

export default {
  name: "VoiceStatus",
  props: {
    asideOpened: {
      type: Boolean
    },
  },
  computed: {
    ...mapState({
      connected: state => state.webrtc.connected,
      status: state => state.webrtc.status,
      streams: state => state.webrtc.streams,
    }),
    translateStatus () {
      switch(this.status) {
        case 'connected':
          return 'Voice connected'
        case 'connecting':
          return 'Connecting voice'
        case 'disconnected':
          return 'Voice disconnected'
        default:
          return 'Voice disconnected'
      }
    },
    icon () {
      switch (this.status) {
        case 'connected':
          return { icon: 'signal', color: '#48c774' }
        case 'connecting':
          return { icon: 'satellite-dish', color: '#ffdd57' }
        case 'disconnect':
          return { icon: 'signal', color: '#f14668' }
        default:
          return { icon: 'signal', color: '#f14668' }
      }
    }
  },
  methods: {
    disconnect () {
      console.log('emit')
      this.$emit('disconnect')
    }
  }
}
</script>
<style lang="scss" scoped>

  .connect-area-voice{
    display: flex !important;
    justify-content: space-between !important;
    margin-top: 3%;
    margin-left: 2%;

    .status-icon {
      margin-right: 4%;
      margin-top: 4%;
    }

    .connect-area-voice-disconnect {
      cursor: pointer;
      margin-left: 3%;
      margin-right: 3%;
      margin-top: 2%;
    }

    .connect-area-voice-status {
      width:80%;
      display: flex;
      justify-content: flex-start;

      .connect-area-voice-status-text {
        display: flex;
        flex-direction: column;
        
        p {
          font-weight: bolder;
          font-size: .90rem;
        }
        span {
          font-size: .80rem;
        }

      }
    }
  }

</style>
