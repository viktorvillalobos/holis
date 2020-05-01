<template>
  <div :class="['connect-card', {'connect-card--outline' : outline}]">
    <slot />
  </div>
</template>
<script>
/**
 * A card to wrap all kind of interest things
 * @displayName Card
 */
export default {
  name: "card",
  props: {
    outline: {
      type: Boolean,
      default: false
    }
  }
};
</script>
<style lang="scss" scoped>
.connect-card {
  box-shadow: $card-box-shadow;
  border-radius: $card-border-radius;
  background-color: #fff;

  &--outline {
    box-shadow: none;
    border: 1px solid;
  }
}
</style>