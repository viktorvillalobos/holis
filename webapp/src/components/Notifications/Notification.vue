<template>
  <div :class="['connect-notification-card']">
    <card outline>
      <div class="connect-notification-image">
        <img src="@/assets/notifications/reminder.png" alt="notifications" />
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
<style lang="scss">
.connect-notification {
  &-image {
    max-width: 30px;
  }
  &-card {
    margin-bottom: 8px;
    .connect-card {
      position: relative;
      display: flex;
      padding: 15px;
    }

    .connect-btn span {
      font-size: 0.7rem;
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
    font-size: .9rem;
    &-action {
      margin-bottom: 0;
      width: 100%;
      display: inline-flex;
      justify-content: flex-end;
    }
  }
}
</style>
