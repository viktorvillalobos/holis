<template>
  <div class="connect-app-container">
    <div class="connect-container">
      <ToolsMenu :aside-opened="isAsideLeftActive" />
      <Logo :aside-opened="isAsideLeftActive" />
      <AsideLeft :name="asideLeftName" :active="isAsideLeftActive">
        <transition name="translate-x">
          <Board v-if="isBoardActive" />
        </transition>
        <transition name="translate-x">
          <Notifications v-if="isNotificationsActive" />
        </transition>
      </AsideLeft>
      <notification-card
        @close="handleNotification"
        :aside-opened="isAsideLeftActive"
        :active="notification.show"
      >{{ notification.text }}</notification-card>
      <AsideRight :active="isAsideRightActive">
        <chat />
      </AsideRight>
      <user-card
        :sound="isSoundActive"
        :micro="isMicroActive"
        @micro="handleMicro"
        @sound="handleSound"
        :float="!isAsideRightActive"
      />
      <chat-bubbles @asideHandle="handleAsideRight" :aside-opened="isAsideRightActive" />
    </div>
    <router-view></router-view>
  </div>
</template>
<script>
import ToolsMenu from "@/components/ToolsMenu";
import Logo from "@/components/Logo";
import NotificationCard from "@/components/Notifications/NotificationCard";
import Notifications from "@/components/Notifications";
import AsideLeft from "@/components/AsideLeft";
import AsideRight from "@/components/AsideRight";
import Board from "@/components/Board";

import UserCard from "@/components/UserCard";
import ChatBubbles from '@/components/Chat/ChatBubbles'
import Chat from '@/components/Chat'

import { mapState } from "vuex";

export default {
  name: "AppContainer",
  components: {
    ToolsMenu,
    Logo,
    Board,
    AsideLeft,
    AsideRight,
    NotificationCard,
    Notifications,
    UserCard,
    ChatBubbles,
    Chat
  },
  computed: {
    ...mapState({
      isAsideLeftActive: state => state.app.isAsideLeftActive,
      isAsideRightActive: state => state.app.isAsideRightActive,
      isBoardActive: state => state.app.isBoardActive,
      isNotificationsActive: state => state.app.isNotificationsActive,
      isMicroActive: state => state.app.isMicroActive,
      isSoundActive: state => state.app.isSoundActive,
      notification: state => state.app.notification
    }),
    asideLeftName() {
      if (this.isNotificationsActive) return "Notificaciones";

      if (this.isBoardActive) return "Cartelera";

      return "Aside";
    }
  },
  data() {
    return {
      showNotification: false
    };
  },
  created() {
    // this.$store.dispatch("getList")
  },
  methods: {
    handleAsideLeft() {
      this.$store.commit("setAsideLeftActive");
    },
    handleAsideRight() {
      this.$store.commit("setAsideRightActive");
    },
    handleMicro() {
      this.$store.commit("setMicroActive");
    },
    handleSound() {
      this.$store.commit("setSoundActive");
    },
    handleNotification() {
      this.showNotification = !this.showNotification;
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

body {
  background: $background;
  font-family: "Ubuntu", sans-serif;
  color: $font-color;
  font-size: 14px;
}

.connect-container * {
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
</style>