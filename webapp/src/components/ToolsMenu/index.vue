<template>
  <div :class="['connect-menu', {'aside-opened' : asideOpened}]">
    <card>
      <ul>
        <li @click="goTo('office')" :class="{'active' : $route.name === 'office'}">
          <span class="material-icons-round">home</span>
        </li>
      <!--
        <li @click="goTo('reports')" :class="{'active' : $route.name === 'reports'}">
          <font-awesome-icon icon="chart-pie" />
      </li>
      -->
        <li @click="goTo('user-config')" :class="{'active' : $route.name.includes('-config')}">
          <span class="material-icons-outlined">settings</span>
        </li>

        <li @click="handleProjects" :class="{'active': isProjectsActive && asideOpened}">
          <span class="material-icons-outlined">list_alt</span>
        </li>
      </ul>
    </card>

    <card class="mt-5">
      <ul>
        <li @click="handleNotifications" :class="{'active': isNotificationsActive && asideOpened}">
          <span class="material-icons-outlined">notifications</span>
        </li>
        <li @click="handleBoard" :class="{'active': isBoardActive && asideOpened}">
          <span class="material-icons-outlined">article</span>
        </li>
        <li @click="handleReleases" :class="{'active': isReleasesActive && asideOpened}">
          <span class="material-icons-outlined">grade</span>
        </li>
      </ul>
    </card>
  </div>
</template>
<script>
import { mapState } from 'vuex'
import Card from '@/components/Card.vue'
export default {
  name: 'ToolsMenu',
  components: {
    Card
  },
  props: {
    asideOpened: {
      type: Boolean
    }
  },
  data () {
    return {}
  },
  computed: {
    ...mapState({
      isBoardActive: state => state.app.isBoardActive,
      isNotificationsActive: state => state.notifications.isNotificationsActive,
      isReleasesActive: state => state.app.isReleasesActive,
      isProjectsActive: state => state.app.isProjectsActive
    })
  },
  methods: {
    handleBoard () {
      const statusAux = this.isBoardActive
      this.closeAllAside()
      if (!this.asideOpened || statusAux) { this.$store.commit('setAsideLeftActive') }
      this.$store.commit('setBoardActive')
      this.$store.dispatch('getList')
      this.$store.dispatch('getBirthdays')
    },
    handleProjects () {
      const statusAux = this.isProjectsActive
      this.closeAllAside()
      if (!this.asideOpened || statusAux) { this.$store.commit('setAsideLeftActive') }
      this.$store.commit('setProjectsActive')
    },
    handleNotifications () {
      const statusAux = this.isNotificationsActive
      this.closeAllAside()
      if (!this.asideOpened || statusAux) { this.$store.commit('setAsideLeftActive') }
      this.$store.commit('setNotificationsActive', !statusAux)
    },
    handleReleases () {
      const statusAux = this.isReleasesActive
      this.closeAllAside()
      if (!this.asideOpened || statusAux) { this.$store.commit('setAsideLeftActive') }
      this.$store.commit('setReleasesActive')
    },
    closeAllAside () {
      this.$store.commit('setNotificationsActive', false)
      this.$store.commit('closeAllAside')
    },
    goTo (to) {
      if (this.$route.name === to) { to = 'office' }
      this.$router.push({ name: to })
    }
  }
}
</script>
<style lang="scss" scoped>
.connect-menu {
  position: fixed;
  top: 100px;
  left: $margin-left-container;
  width: 50px;
  transition: $aside-transition;

  &.aside-opened {
    left: $margin-left-container-aside-opened;
  }

  .connect-card {
    margin-bottom: 15px;
  }

  ul {
    padding: 10px 5px;
    margin: 0 auto;
    list-style: none;

    li {
      margin: 0 auto;
      width: 40px;
      height: 40px;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #BDBDBD;
      svg {
        z-index: 2;
      }

      &:hover {
        cursor: pointer;
        color: $primary;
      }

      &.active {
        color: $primary;
      }
    }
  }
}
</style>
