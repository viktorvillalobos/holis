<template>
  <card :class="['connect-aside-left', {'aside-opened' : active}]">
    <slot>Holi! Soy el aside de la izquierda, aqui puedes poner lo que quieras :DDDD</slot>
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
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../assets/variables";
.connect-aside-right {
  width: $aside-width;
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  margin-right: -100%;
  transition: $aside-transition;

  &.aside-opened {
    margin-right: 0;
  }
}
</style>