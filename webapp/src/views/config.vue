<template>
  <div class="holis-config pl-5 pt-6">
    <div class="columns">
      <div class="column is-2">
        <div class="config-links-container">
          <b class="is-size-4">Settings</b>
          <ul class="holis-config-links mt-3">
            <li>
              <router-link exact :to="{name: 'user-config'}">Profile</router-link>
            </li>
            <li>
              <router-link exact :to="{name: 'voice-and-video-config'}">Voice and Video</router-link>
            </li>
            <li>
              <router-link exact :to="{name: 'notifications-config'}">Notifications</router-link>
            </li>
            <li>
              <router-link exact :to="{name: 'users-role-config'}">Users</router-link>
            </li>
          </ul>
        </div>
      </div>
      <div class="column">
        <card class="holis-config-card" outline>
          <router-view />
        </card>
      </div>
    </div>
  </div>
</template>

<script>
import Card from '@/components/Card'

export default {
  name: 'configView',
  components: {
    Card
  }
}
</script>

<style lang="scss" scoped>
.holis-config {
  font-family: $family-dm-sans;
  &-links {
    .router-link-active {
      font-weight: 900;
    }

    li {
      margin-bottom: 0.8rem;
    }
  }

  .config-links-container {
    position: fixed;
  }
}
</style>
