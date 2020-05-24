<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>

window.onbeforeunload = function(e) {
    e = e || window.event;

    // For IE and Firefox prior to version 4
   if (e) {
        e.returnValue = 'Sure?';
   }
   return 'Dialog text here.';
};

export default {
  name: "App",
  created() {
  },
  mounted() {
  },
  methods: {
  }
};
</script>

<style lang="scss">
</style>
