<template>
  <div class="connect-avatar-wrapper">
    <div :class="['connect-avatar', status, {'connect-avatar--bigger': big}, {'connect-avatar--huge': huge}]" :style="`background-image: url(${img})`">
      <slot />
    </div>
    <span v-if="text">{{text}}</span>
  </div>
</template>
<script>
/**
 * A simple avatar to show off that cute face you have ;)
 * @displayName Avatar
 */
export default {
  name: 'avatar',
  props: {
    /**
     * The route where the img of the avatar is hosted
     */
    img: {
      type: String,
      default: ''
    },
    /**
     * A text that will be rendered under the avatar
     */
    text: {
      type: String
    },
    /**
     * A status to show if the user is somehow available, if not included wont show the user status
     * @values available, busy, disconnected
     */
    status: {
      type: String
    },
    /**
     * Increases the size of the avatar
     */
    big: {
      type: Boolean
    },
    /**
     * Increases a lot the size of the avatar
     */
    huge: {
      type: Boolean
    }
  }
}
</script>
<style lang="scss" scoped>
.connect-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background-size: cover;
  position: relative;

  &:after {
    content: '';
    width: 6px;
    height: 6px;
    position: absolute;
    top: 8px;
    right: 8px;
    border-radius: 50%;
  }

  &.available {
    &:after {
      background-color: greenyellow;
    }
  }

  &--bigger {
    width: 70px;
    height: 70px;

    &:after {
      width: 12px;
      height: 12px;
      top: 5px;
      right: 5px;
    }
  }

  &--huge {
    width: 114px;
    height: 114px;

    &:after {
      width: 12px;
      height: 12px;
      top: 5px;
      right: 5px;
    }
  }

  &-wrapper {
    max-width: 42px;
    text-align: center;
    span {
      display: block;
      width: 100%;
      font-size: 10px;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }
}
</style>
