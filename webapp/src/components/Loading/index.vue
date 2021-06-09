<template>
  <div class="main-loader">
      <div :class="{'card' : true, 'loader-wrapper' : true, 'is-active' : loading}">
        <div class="card-content">
          <div class="loader is-loading"></div>
        </div>
      </div>
    </div>
</template>
<script>
import { mapState } from 'vuex'
import Card from "@/components/Card";

export default {
  name: "Loading",
  components: {
    Card
  },
  props:["loading"],
  data(){
    return {}
  },
  computed: {
    ...mapState({
      currentScreen: state => state.projects.currentScreen
    })
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.main-loader{
    width:100%;
    height:100%; 
}
.loader-wrapper {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100px;
    height: 100px;
    margin-top: -50px; /* Half the height */
    margin-left: -50px; /* Half the width */
    background: #fff;
    opacity: 0;
    z-index: -1;
    transition: opacity .3s;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 6px;

    .loader {
        height: 80px;
        width: 80px;
    }

    &.is-active {
        opacity: 1;
        z-index: 1;
    }
}
</style>