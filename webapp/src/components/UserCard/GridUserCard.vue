<template>
  <div :class="['connect-grid-user-card', origin]" 
        @mouseover="onMouseOver()" 
        @mouseleave="onMouseLeave()">
    <img src="@/assets/gridUserCardWaves.svg" class="connect-grid-user-card-waves" />
    <div class="connect-grid-user-card-content">
      <Avatar big
              :img="img"/>
      <div class="connect-grid-user-card-content-info">
        <h3>{{ name }}</h3>
        <p class="position">{{ position }}</p>
        <p class="status">
          {{ status.icon_text }} {{ status.text }}
        </p>
      </div>
    </div>
    <ul class="connect-grid-user-card-actions">
      <li v-if="!isLocalUser">
        <Btn primary @btn-click="onChat()">Chat</Btn>
      </li>
    </ul>
  </div>
</template>
<script>
import Avatar from '@/components/Avatar'
import Btn from '@/components/Btn'
import _ from 'lodash'
export default {
  name: 'GridUserCard',
  props: {
    origin: {
      type: String,
      default: 'top'
    },
    isLocalUser: {
      type: Boolean,
      default: false
    },
    name: {
      type: String,
      default: 'Johana Daivis'
    },
    position: {
      type: String,
      default: 'UX / UI Desginer'
    },
    status: {
      type: Object,
      default: () => {
        return {'text': 'working', 'icon': ''}
      }
    },
    img: {
      type: String,
      default: 'https://api.adorable.io/avatars/71/abott@adorable.png'
    },
    user: {
      type: Object,
      default: () => {
        return null
      }
    }
  },
  components: {
    Avatar,
    Btn
  },
  methods: {
    onChat() {
      this.$emit('onChat', this.user)
    },
    onMouseOver: _.debounce(function() {
      this.$emit('onMouseOver')
    }, 200),
    onMouseLeave: _.debounce(function() {
      this.$emit('onMouseLeave')
    }, 200)
  }
}
</script>
<style lang="scss" scoped>
.connect-grid-user-card {
  width: 300px;
  height: 150px;
  border-radius: 8px;
  background: #fff;
  position: absolute;

  &:before {
    content: "";
    display: block;
    width: 16px;
    height: 16px;
    position: absolute;
    transform: rotate(45deg);
  }

  &.top {
    &:before {
      top: -8px;
      left: calc(50% - 8px);
      background-color: $primary;
    }
  }

  &.left {
    &:before {
      left: -8px;
      top: calc(50% - 8px);
      background-color: #9b51e0;
    }
  }

  &.right {
    &:before {
      right: -8px;
      top: calc(50% - 8px);
      background-color: #fff;
    }
  }

  &.bottom {
    &:before {
      bottom: -8px;
      left: calc(50% - 8px);
      background-color: #fff;
    }
  }

  &-waves {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1;
    border-radius: 8px 8px 0 0;
  }

  &-content {
    position: relative;
    z-index: 3;
    width: 100%;
    padding: 10px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 10px;

    &-info {
      color: #fff;
      width: 190px;

      h3 {
        font-size: 16px;
      }

      .position {
        font-size: 14px;
        margin-bottom: 9px;
      }

      .status {
        font-size: 12px;
        color: #000;
      }
    }
  }

  &-actions {
    padding: 0 10px 10px 10px;
    width: 100%;
    display: inline-flex;
    align-items: center;
    justify-content: flex-end;
  }
}
</style>
