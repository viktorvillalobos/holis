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
        :user="user"
      />
      <chat-bubbles @asideHandle="handleAsideRight" :aside-opened="isAsideRightActive" />

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
            :style="`mask-image: url(${publicPath}/Vector.svg);`"
          />
        </card>
      </modal>
    </div>
    <div :class="['connect-content-wrapper', {'wrap' : $route.name !== 'office' }]">
      <router-view></router-view>
    </div>
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
import ChatBubbles from "@/components/Chat/ChatBubbles";
import Chat from "@/components/Chat";
import Modal from "@/components/Modal";
import Card from "@/components/Card";

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
    Chat,
    Modal,
    Card
  },
  computed: {
    ...mapState({
      isAsideLeftActive: state => state.app.isAsideLeftActive,
      isAsideRightActive: state => state.app.isAsideRightActive,
      isBoardActive: state => state.app.isBoardActive,
      isNotificationsActive: state => state.app.isNotificationsActive,
      isMicroActive: state => state.app.isMicroActive,
      isSoundActive: state => state.app.isSoundActive,
      notification: state => state.app.notification,
      user: state => state.app.user
    }),
    asideLeftName() {
      if (this.isNotificationsActive) return "Notificaciones";

      if (this.isBoardActive) return "Cartelera";

      return "Aside";
    }
  },
  data() {
    return {
      showNotification: false,
      firstTime: false,
      publicPath: process.env.BASE_URL
    };
  },
  created() {
    // this.$store.dispatch("getList")
  },
  mounted() {
    if (!localStorage.firstTime) {
      this.firstTime = true;
    }
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
    },
    handleFirstTime() {
      localStorage.firstTime = false;
      this.firstTime = false;
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
    width: calc(100% - #{$aside-width + $menus-width});
    margin-left: $menus-width;
    margin-top: 75px;
    padding: 0 20px;
  }
}
</style>