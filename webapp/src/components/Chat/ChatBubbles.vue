<template>
  <ul :class="['connect-chat-bubbles', {'aside-opened': asideOpened}]">
    <li>
      <Btn @btn-click="emitAsideHandle" :size="30" primary round icon>
        <svg
          v-if="asideOpened"
          width="5"
          height="9"
          viewBox="0 0 5 9"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g clip-path="url(#clip0)">
            <path
              d="M0.625 8.125L4.375 4.375L0.625 0.625"
              stroke="white"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </g>
          <defs>
            <clipPath id="clip0">
              <rect width="5" height="8.75" fill="white" />
            </clipPath>
          </defs>
        </svg>
        <svg
          v-else
          width="5"
          height="9"
          viewBox="0 0 5 9"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g clip-path="url(#clip0)">
            <path
              d="M4.375 8.125L0.625 4.375L4.375 0.625"
              stroke="white"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </g>
          <defs>
            <clipPath id="clip0">
              <rect width="5" height="8.75" transform="matrix(-1 0 0 1 5 0)" fill="white" />
            </clipPath>
          </defs>
        </svg>
      </Btn>
    </li>
    <li>
      <Btn :size="40" primary round icon @btn-click="newChat">
        <font-awesome-icon icon="comment-medical" />
      </Btn>
    </li>
    <li>
      <Avatar />
    </li>

    <li>
      <Avatar />
    </li>

    <li>
      <Avatar />
    </li>
  </ul>
</template>
<script>
import Avatar from "@/components/Avatar";
import Btn from "@/components/Btn";
export default {
  name: "ChatBubbles",
  props: {
    asideOpened: {
      type: Boolean
    }
  },
  components: {
    Avatar,
    Btn
  },
  methods: {
    emitAsideHandle () {
      this.$emit('asideHandle')
    },
    newChat () {
      console.log('newChat')
      this.$emit('newChat')
    }
  }
};
</script>
<style lang="scss" scoped>
.connect-chat-bubbles {
  position: fixed;
  bottom: 11px;
  right: 16px;
  width: 45px;
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: $aside-transition;

  &.aside-opened {
    right: 341px;
  }

  li {
    margin: 7px 0;
    cursor: hover;
  }
}
</style>
