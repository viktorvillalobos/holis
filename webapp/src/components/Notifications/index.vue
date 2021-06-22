<template>
  <div class="connect-notification-list">
    <Loading v-bind:loading="loading"/>
    <Notification v-for="(ntf, index) in notifications" :key="index" v-bind:notification="ntf">
      <div v-html="ntf.description"></div>
    </Notification>
  </div>
</template>
<script>
import { mapState } from 'vuex'
import Notification from './Notification'
import Loading from '@/components/Loading'

export default {
  name: 'NotificationsList',
  data(){
    return {
      loading: true
    }
  },
  components: {
    Notification,
    Loading
  },
  created () {
    this.getNotifications()
  },
  computed: {
    ...mapState({
      notifications: state => state.notifications.notifications
    })
  },
  watch: {
    notifications : function(notifications){
      this.loading = false
      console.log(notifications)
    }
  },
  methods: {
    getNotifications () {
      this.loading = true
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
