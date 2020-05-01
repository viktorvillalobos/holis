<template>
  <div class="connect-avatar-wrapper">
    <div :class="['connect-avatar', status]" :style="`background-image: url(${img})`">
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
  name: "avatar",
  props: {
    /**
     * The route where the img of the avatar is hosted
     */
    img: {
      type: String,
      default: "https://api.adorable.io/avatars/50/abott@adorable.png"
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
    }
  }
};
</script>
<style lang="scss" scoped>
.connect-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background-size: cover;

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