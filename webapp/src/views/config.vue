<template>
  <div class="holis-config">
    <div class="columns">
      <div class="column">
        <h1>Configuraciones</h1>
      </div>
    </div>
    <div class="columns">
      <div class="column is-2">
        <ul class="holis-config-links">
          <li>
            <router-link exact :to="{name: 'user-config'}">Usuario</router-link>
          </li>
          <li>
            <router-link exact :to="{name: 'voice-and-video-config'}">Voz y video</router-link>
          </li>
          <li>
            <router-link exact :to="{name: 'notifications-config'}">Notificaciones</router-link>
          </li>
        </ul>
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
  &-links {
    text-align: right;

    .router-link-active {
      font-weight: 900;
    }

    li {
      margin-bottom: 0.8rem;
    }
  }

  &-card {
    padding: 50px 30px;
  }
}
</style>
