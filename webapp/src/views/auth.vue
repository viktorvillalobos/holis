<template>
  <div class="auth-wrapper" :style="`background-image: url(${bg})`">
    <card class="auth-card">
      <img class="auth-logo" src="/static/images/Holis.svg" />
      <router-view />
    </card>
  </div>
</template>
<script>
import Card from "@/components/Card";
import authBg from "@/assets/bg.svg";
export default {
  name: "Login",
  components: {
    Card
  },
  data() {
    return {
      bg: authBg
    };
  }
};
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
</style>
