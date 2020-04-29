<template>
  <card :class="['connect-aside-left', {'aside-opened' : active}]">
    <div class="connect-aside-left-header">
      <h2>{{name}}</h2>
      <div @click="$store.commit('setAsideLeftActive')" class="connect-aside-left-close">
        <img src="@/assets/icons/Close.svg" />
      </div>
    </div>
    <slot></slot>
  </card>
</template>

<script>
import Card from "@/components/Card";
export default {
  name: "AsideLeft",
  components: {
    Card
  },
  props: {
    active: {
      type: Boolean
    },
    name: {
      type: String,
      default: 'Aside'
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../assets/variables";
.connect-aside-left {
  width: $aside-width;
  position: fixed;
  top: 0;
  left: 0;
  margin-left: -100%;
  bottom: 0;
  transition: $aside-transition;

  &-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 5px 10px;
    border-bottom: 1px solid $light-gray;

    h2 {
      margin: 0;
    }
  }

  &-close {
    cursor: pointer
  }

  &.aside-opened {
    margin-left: 0;
  }
}
</style>