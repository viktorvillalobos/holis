<template>
<div class="office">
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
      >
        {{ notification.text }}
      </notification-card>
    </div>
    <div class="connect-office-view">
        <hexagonal-grid :size="38" />
    </div>
  </div>
</template>
<script>
import ToolsMenu from "@/components/ToolsMenu";
import Logo from "@/components/Logo";
import NotificationCard from "@/components/Notifications/NotificationCard";
import Notifications from "@/components/Notifications";
import AsideLeft from "@/components/AsideLeft";
import Board from "@/components/Board";
import HexagonalGrid from '@/components/HexagonalGrid'

import { mapState } from "vuex";

export default {
    name: 'Office',
    components: {
        HexagonalGrid,
        ToolsMenu,
        Logo,
        Board,
        AsideLeft,
        NotificationCard,
        Notifications
    },
  computed: {
    ...mapState({
      isAsideLeftActive: state => state.app.isAsideLeftActive,
      isBoardActive: state => state.app.isBoardActive,
      isNotificationsActive: state => state.app.isNotificationsActive,
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
    handleNotification() {
      this.showNotification = !this.showNotification;
    }
  }
}
</script>
<style lang="scss">

@import url("https://fonts.googleapis.com/css2?family=Ubuntu:wght@400;500;700&display=swap");
@import "../assets/variables";

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
