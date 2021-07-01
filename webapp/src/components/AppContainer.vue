<template>
  <div class="connect-app-container">
    <div class="connect-container">
      <ToolsMenu :aside-opened="isAsideLeftActive" />
      <Logo :aside-opened="isAsideLeftActive" :company="company" />
      <AsideLeft :name="asideLeftName" :active="isAsideLeftActive">
        <transition name="translate-x">
          <Board v-if="isBoardActive" />
        </transition>
        <transition name="translate-x">
          <Notifications v-if="isNotificationsActive" />
        </transition>
        <transition name="translate-x">
          <Projects v-if="isProjectsActive" />
        </transition>
        <transition name="translate-x">
          <Releases v-if="isReleasesActive" />
        </transition>
      </AsideLeft>
      <AreaOptions
        :items="areas.list"
        :current="areas.currentArea"
        :aside-opened="isAsideLeftActive"
        @change="changedArea"
      />
      <notification-card
        @close="handleNotification"
        :aside-opened="isAsideLeftActive"
        :active="notification.show"
      ><span v-html="notification.text"/></notification-card>
      <AsideRight :active="isAsideRightActive">
        <chat @selectedChat="selectedChat" />
      </AsideRight>
      <user-card
        :sound="isSoundActive"
        :micro="isMicroActive"
        :video="isVideoActive"
        @video="handleVideo"
        @micro="handleMicro"
        @sound="handleSound"
        :float="!isAsideRightActive"
        :user="user"
      />
      <chat-bubbles
        @asideHandle="handleAsideRight"
        :aside-opened="isAsideRightActive"
      />

      <modal :active="firstTime" @close="handleFirstTime">
        <card class="welcome-card">
          <h2>¡Hola! 😁</h2>
          <h3>
            Posicionate junto a cualquiera de tus compañeros e inicia un
            <strong>canal de comunicación instantáneamente</strong>
          </h3>
          <img class="vector-bg" src="@/assets/VectorBack.svg" />
          <img
            src="@/assets/peek.gif"
            alt
            class="welcome-gif"
            :style="`mask-image: url(${modalMask});`"
          />
        </card>
      </modal>

      <div :class="['modal', {'is-active' : alert.active}]">
        <div class="modal-background"></div>
        <div class="modal-content">
          <div class="notification connect-alert-notification">
            <button @click="closeAlert" class="delete"></button>
            <div class="connect-alert-content-wrapper">
              <div class="connect-alert-content-icon">
                <font-awesome-icon :icon="alert.icon" :style="{ color: '#5d6de8' }" size="4x" />
              </div>
              <div class="connect-alert-content">
                <h2>{{alert.title}}</h2>
                <p>{{alert.text}}</p>
                <label class="checkbox">
                  <input type="checkbox" />
                  Remember my decision
                </label>
              </div>
            </div>
            <div class="buttons is-right">
              <button @click="closeAlert" class="button">Cancel</button>
              <button @click="closeAlert" class="button is-primary">I'm sure</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div :class="['connect-content-wrapper', {'wrap' : $route.name !== 'office' }]">
      <router-view></router-view>
    </div>
  </div>
</template>
<script>
import ToolsMenu from '@/components/ToolsMenu'
import Logo from '@/components/Logo'
import NotificationCard from '@/components/Notifications/NotificationCard'
import Notifications from '@/components/Notifications'
import Projects from './Projects/index'
import AsideLeft from '@/components/AsideLeft'
import AsideRight from '@/components/AsideRight'
import Board from '@/components/Board'
import AreaOptions from '@/components/AreaOptions'
import Releases from '@/components/Releases'
import UserCard from '@/components/UserCard'
import ChatBubbles from '@/components/Chat/ChatBubbles'
import Chat from '@/components/Chat'
import Modal from '@/components/Modal'
import Card from '@/components/Card'

import { mapState } from 'vuex'

import modalMask from '@/assets/modalMask.svg'

export default {
  name: 'AppContainer',
  components: {
    ToolsMenu,
    Logo,
    Board,
    AreaOptions,
    AsideLeft,
    AsideRight,
    NotificationCard,
    Notifications,
    Releases,
    UserCard,
    ChatBubbles,
    Chat,
    Modal,
    Card,
    Projects
  },
  computed: {
    ...mapState({
      isAsideLeftActive: state => state.app.isAsideLeftActive,
      isAsideRightActive: state => state.app.isAsideRightActive,
      isBoardActive: state => state.app.isBoardActive,
      isNotificationsActive: state => state.notifications.isNotificationsActive,
      isReleasesActive: state => state.app.isReleasesActive,
      isProjectsActive: state => state.app.isProjectsActive,
      isVideoActive: state => state.app.isVideoActive,
      isMicroActive: state => state.app.isMicroActive,
      isSoundActive: state => state.app.isSoundActive,
      notification: state => state.notifications.notification,
      user: state => state.app.user,
      users: state => state.chat.users,
      areas: state => state.areas,
      alert: state => state.app.alert
    }),
    asideLeftName () {
      if (this.isNotificationsActive) return 'Notificaciones'

      if (this.isBoardActive) return 'Cartelera'

      if (this.isReleasesActive) return 'Novedades'

      if (this.isProjectsActive) return 'Proyectos'

      return 'Aside'
    },
    company () {
      return {
        name: this.user ? this.user.company.name : null,
        logo: this.user ? this.user.company.logo_thumb : null
      }
    }
  },
  data () {
    return {
      firstTime: false,
      publicPath: process.env.BASE_URL,
      modalMask
    }
  },
  mounted () {
    if (!localStorage.firstTime) {
      this.firstTime = true
    }
    this.gets()
  },
  methods: {
    gets () {
      this.getUsers()
      //this.getRecents()
    },
    getUsers () {
      try {
        this.$store.dispatch('getUsers')
      } catch (e) {
        console.log('couldnt load users')
      }
    },
    getRecents  () {
      try {
        this.$store.dispatch('getRecents',"")
      } catch (e) {
        console.log('couldnt load recents')
      }
    },
    handleAsideLeft () {
      this.$store.commit('setAsideLeftActive')
    },
    handleAsideRight () {
      this.$store.commit('setAsideRightActive')
    },
    handleVideo () {
      this.$store.commit('setVideoActive')
    },
    handleMicro () {
      this.$store.commit('setMicroActive')
    },
    handleSound () {
      this.$store.commit('setSoundActive')
    },
    handleNotification () {
      this.$store.commit('closeActiveNotification')
    },
    handleFirstTime () {
      localStorage.firstTime = false
      this.firstTime = false
    },
    changedArea (area) {
      const filtered = this.areas.list.filter(x => x.name === area)
      if (filtered[0]) this.$store.commit('setNewCurrent', filtered[0])
    },
    newChat () {
      if (!this.isAsideRightActive) this.handleAsideRight()
      this.$store.commit('setChatActive', true)
    },
    selectedChat () {
      this.$store.commit('setChatActive', false)
    },
    closeAlert () {
      const alert = {
        active: false,
        text: 'Are you sure you wanna get out of this voice channel?',
        title: 'Wait!',
        icon: 'grin-beam-sweat'
      }

      this.$store.commit('setAlert', alert)
    }
  }
}
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

body {
  background: $background;
  font-family: "Ubuntu", sans-serif;
  color: $font-color;
  font-size: 14px;
}

.connect-container > * {
  z-index: 15;
}

h1,
h2,
h3,
h4 {
  font-weight: 400;
}

h1 {
  font-size: 24px;
}

h2 {
  font-size: 22px;
}

h3 {
  font-size: 18px;
}

h4 {
  font-size: 16px;
}

a {
  color: $primary;
  cursor: pointer;
}

.translate-y-enter-active {
  transition: all 0.3s ease;
}
.translate-y-enter, .translate-y-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateY(10px);
  opacity: 0;
}

.translate-x-enter-active {
  transition: all 0.3s;
}

.translate-x-enter, .translate-y-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(-20px);
  opacity: 0;
}

.connect-card.welcome-card {
  position: relative;
  height: 380px;
  overflow: hidden;
  padding: 15px;
  text-align: center;
  border-radius: 8px;

  h2 {
    font-weight: 600;
    color: $primary;
    font-size: 20px;
  }
}

.welcome-gif {
  left: 0;
  position: absolute;
  mask-size: 100%;
  mask-repeat: no-repeat;
  mask-position-y: -60px;
  -webkit-mask-size: 100%;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position-y: -60px;
}

.vector-bg {
  position: absolute;
}

.connect-content-wrapper {
  &.wrap {
    width: calc(115% - #{$aside-width + $menus-width});
    margin-left: $menus-width;
    margin-top: 75px;
    padding: 0 20px;
  }
}

.connect-alert-content {
  &-wrapper {
    display: flex;
    margin-bottom: 30px;
  }

  &-icon {
    margin-right: 25px;
  }

  h2 {
    font-size: 1.25rem;
  }

  .checkbox {
    margin-top: 20px;
  }
}

.connect-alert-notification {
  max-width: 490px;
  margin: 0 auto;
}
</style>
