<template>
  <div :class="['connect-logo-wrapper', {'aside-opened' : asideOpened}]">
    <svg
      v-if="!company.logo"
      class="connect-logo"
      width="50"
      height="47"
      viewBox="0 0 50 47"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g style="mix-blend-mode:multiply">
        <path
          d="M39.824 14.8728C39.824 23.0868 33.1652 29.7456 24.9512 29.7456C16.7371 29.7456 10.0784 23.0868 10.0784 14.8728C10.0784 6.65878 16.7371 0 24.9512 0C33.1652 0 39.824 6.65878 39.824 14.8728Z"
          fill="#EB5757"
        />
      </g>
      <g style="mix-blend-mode:multiply">
        <path
          d="M29.7456 31.5068C29.7456 39.7209 23.0868 46.3796 14.8728 46.3796C6.65878 46.3796 0 39.7209 0 31.5068C0 23.2928 6.65878 16.634 14.8728 16.634C23.0868 16.634 29.7456 23.2928 29.7456 31.5068Z"
          fill="#27AE60"
        />
      </g>
      <g style="mix-blend-mode:multiply">
        <path
          d="M50 31.5068C50 39.7209 43.3412 46.3796 35.1272 46.3796C26.9132 46.3796 20.2544 39.7209 20.2544 31.5068C20.2544 23.2928 26.9132 16.634 35.1272 16.634C43.3412 16.634 50 23.2928 50 31.5068Z"
          fill="#2F80ED"
        />
      </g>
    </svg>

    <img v-if="company.logo" class="connect-logo-company" :src=" company.logo" :alt="company.name" width="50"/>
    <h1 class="connect-company">{{company.name}}</h1>
  </div>
</template>

<script>
/**
 * The wrapper of the logos :D
 * @displayName Logo
 */
export default {
  name: "Logo",
  props: {
    /**
     * The data of the company name and logo, if logo is not provided it will be replaced by the company name as text
     */
    company: {
      type: Object,
      default: () => {
        return {
          name: "Tacata Inc.",
          logo: null
        };
      }
    },
    asideOpened: {
      type: Boolean
    }
  }
};
</script>

<style lang="scss" scoped>
.connect-logo {
  max-height: 46px;
  &-wrapper {
    display: flex;
    position: fixed;
    top: 0;
    left: $margin-left-container;
    align-items: center;
    justify-content: center;
    padding: 7px 9px 7px 0;
    transition: $aside-transition;

    &.aside-opened {
      left: $margin-left-container-aside-opened;
    }

    .connect-company {
      font-weight: bold;
      font-size: 24px;
      line-height: 28px;
      margin: 0 0 0 14px;
    }
  }
}
</style>
