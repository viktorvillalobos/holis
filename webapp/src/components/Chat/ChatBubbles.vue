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
      <Btn :size="40" primary round icon>
        <svg
          width="34"
          height="34"
          viewBox="0 0 34 34"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g clip-path="url(#clip0)">
            <path
              d="M17.997 17.9676L24.0711 17.9746C24.3374 17.9746 24.5927 17.8688 24.7811 17.6805C24.9694 17.4922 25.0751 17.2368 25.0751 16.9705C25.0751 16.7042 24.9694 16.4489 24.7811 16.2605C24.5927 16.0722 24.3374 15.9665 24.0711 15.9665L17.997 15.9735L18.0041 9.89948C18.0041 9.63318 17.8983 9.37778 17.71 9.18948C17.5217 9.00117 17.2663 8.89539 17 8.89539C16.7337 8.89539 16.4783 9.00117 16.29 9.18948C16.1017 9.37778 15.9959 9.63318 15.9959 9.89948L16.003 15.9735L9.92892 15.9665C9.79691 15.9659 9.6661 15.9915 9.54403 16.0418C9.42196 16.0921 9.31106 16.166 9.21771 16.2593C9.12437 16.3527 9.05043 16.4636 9.00016 16.5857C8.94989 16.7077 8.92429 16.8385 8.92483 16.9705C8.92429 17.1026 8.94989 17.2334 9.00016 17.3554C9.05042 17.4775 9.12437 17.5884 9.21771 17.6818C9.31106 17.7751 9.42196 17.849 9.54403 17.8993C9.6661 17.9496 9.79691 17.9752 9.92892 17.9746L16.003 17.9676L15.9959 24.0416C15.9954 24.1736 16.021 24.3044 16.0712 24.4265C16.1215 24.5486 16.1954 24.6595 16.2888 24.7528C16.3821 24.8462 16.493 24.9201 16.6151 24.9704C16.7372 25.0206 16.868 25.0462 17 25.0457C17.132 25.0462 17.2628 25.0206 17.3849 24.9704C17.5069 24.9201 17.6178 24.8462 17.7112 24.7528C17.8045 24.6595 17.8785 24.5486 17.9287 24.4265C17.979 24.3044 18.0046 24.1736 18.0041 24.0416L17.997 17.9676Z"
              fill="white"
            />
          </g>
          <defs>
            <clipPath id="clip0">
              <rect x="17" width="24" height="24" transform="rotate(45 17 0)" fill="white" />
            </clipPath>
          </defs>
        </svg>
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