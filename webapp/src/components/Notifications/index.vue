<template>
  <div class="connect-notification-list">
    <Notification v-for="(ntf, index) in notifications" :key="index">
      <div v-html="ntf.description"></div>
    </Notification>
  </div>
</template>
<script>
import { mapState } from 'vuex'
import Notification from './Notification'
export default {
  name: 'NotificationsList',
  components: {
    Notification
  },
  created () {
    this.getNotifications()
  },
  computed: {
    ...mapState({
      notifications: state => state.app.notifications
    })
  },
  methods: {
    getNotifications () {
      try {
        this.$store.dispatch('getNotifications')
      } catch (e) {
        console.log('couldnt load notifications')
      }
    }
  }
}
</script>
<style lang="scss" scoped>
.connect-notification-list {
  padding: 15px;
}
</style>
