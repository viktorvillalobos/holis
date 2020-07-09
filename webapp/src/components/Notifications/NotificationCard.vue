<template>
  <transition name="translate-y">
    <div v-if="active" :class="['connect-notification-card' , {'aside-opened' : asideOpened}]">
      <card>
        <div class="connect-notification-image">
          <img src="@/assets/notifications/reminder.png" alt="notifications" />
        </div>
        <div @click="handleClose" class="connect-notification-close">
          <img src="@/assets/icons/Close.svg" />
        </div>
        <div class="connect-notification-content">
          <div class="connect-notification-content-body">
            <slot />
          </div>
          <ul class="connect-notification-content-action">
            <li>
              <btn flat>Informar ausencia</btn>
            </li>
            <li>
              <btn primary>¡Entrar ya!</btn>
            </li>
          </ul>
        </div>
      </card>
    </div>
  </transition>
</template>
<script>
import Card from '@/components/Card'
import Btn from '@/components/Btn'
export default {
  name: 'NotificationCard',
  props: {
    active: {
      type: Boolean,
      default: false
    },
    img: {
      type: String
    },
    asideOpened: {
      type: Boolean
    }
  },
  components: {
    Card,
    Btn
  },
  methods: {
    handleClose () {
      this.$emit('close')
    }
  }
}
</script>
<style lang="scss" scoped>
.connect-notification {
  &-card {
    position: fixed;
    bottom: 48px;
    left: $margin-left-container;
    width: 400px;
    max-width: 90%;
    transition: $aside-transition;

    &.aside-opened {
      left: $margin-left-container-aside-opened;
    }

    .connect-card {
      position: relative;
      display: flex;
      padding: 15px;
    }

    ul {
      list-style: none;
      padding: 0;

      li {
        margin-left: 10px;
      }
    }
  }

  &-close {
    position: absolute;
    top: 4px;
    right: 4px;
    cursor: pointer;
    z-index: 3;
  }

  &-content {
    margin-left: 10px;
    &-action {
      margin-bottom: 0;
      width: 100%;
      display: inline-flex;
      justify-content: flex-end;
    }
  }
}
</style>
