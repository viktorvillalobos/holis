<template>
  <div :class="['connect-area-voice', {'aside-opened' : asideOpened}]">
    <font-awesome-icon :color="icon.color" :icon="icon.icon" class="status-icon"/> 
    <span>{{ status[0].toUpperCase() + status.slice(1,) }}</span>
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
      status: state => state.webrtc.status
    }),
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
  }
}
</script>
<style lang="scss" scoped>
.connect-area-voice{
  position: fixed;
  bottom: 50px;
  display: flex;
  align-items: center;
  left: $margin-left-container;
  transition: $aside-transition;
  margin-left: 10px;

  &.aside-opened {
    left: $margin-left-container-aside-opened;
  }

  .status-icon {
    margin-right: 14%;
  }
}

</style>
