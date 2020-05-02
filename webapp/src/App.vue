<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  created() {
    this.$store.dispatch("getList")
    this.$store.dispatch("getAreas")
  },
};
</script>

<style lang="scss">
</style>
