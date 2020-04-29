<template>
  <transition name="translate-y" >
    <div class="login-wrapper">
      <div class="login">
        <div class="field">
        <p class="control has-icons-left has-icons-right">
          <input class="input" type="text" placeholder="Company or team name">
          <span class="icon is-small is-left">
            <i class="fas fa-envelope"></i>
          </span>
          <span class="icon is-small is-right">
            <i class="fas fa-check"></i>
          </span>
        </p>
      </div>
      <div class="field">
        <p class="control">
          <button class="button is-success">
            Next
          </button>
        </p>
      </div>
      </div>
    </div>
  </transition>
</template>
<script>
export default {
  name: 'Login',
}
</script>

<style lang="scss">
  .login-wrapper {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;

    .field {
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }

</style>
