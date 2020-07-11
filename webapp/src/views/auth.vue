<template>
  <div class="auth-wrapper" :style="`background-image: url(${bg})`">
    <card class="auth-card">
      <img class="auth-logo" src="/static/images/logo/logo.svg" />
      <router-view />
    </card>
  </div>
</template>
<script>
import Card from '@/components/Card'
import authBg from '@/assets/bg.svg'
export default {
  name: 'Login',
  components: {
    Card
  },
  data () {
    return {
      bg: authBg
    }
  }
}
</script>

<style lang="scss">
.auth {
  &-wrapper {
    padding-top: 130px;
    min-height: 100vh;
    background-size: 100%;
  }

  &-card {
    width: 834px;
    margin: 0 auto;
    padding: 40px 65px;
    position: relative;

    .field-label {
      text-align: left;
    }
    .file-label {
      width: 100%;

      .file-name {
        max-width: none;
      }
    }

    .field:not(:last-child) {
      margin-bottom: 24px;
    }

    form {
      margin: 0 auto;
      max-width: 70%;

      h3 {
        font-size: 1.5rem;
        font-weight: 500;
        margin-bottom: 24px;
      }
    }
  }

  &-logo {
    position: absolute;
    top: -49px;
    left: 18px;
  }

  &-options {
    display: flex;
    justify-content: flex-end;

    & > * {
      margin-left: 16px;
    }
  }
}

.onboarding {
  &-stepper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    span {
      vertical-align: middle;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      border-radius: 50%;
      color: #fff;
      width: 39px;
      height: 39px;
      font-size: 24px;
      margin-right: 16px;
      background: #bdbdbd;
    }

    li {
      display: flex;
      align-items: center;

      &.active {
        font-size: 24px;
        font-weight: 500;
        span {
          width: 59px;
          height: 59px;
          font-size: 48px;
          background: $primary;
        }
      }
    }
  }
}
</style>
