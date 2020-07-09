<template>
  <div v-if="active" :class="['modal', {'is-active' : active}]">
    <div class="modal-background"></div>
    <div class="modal-content">
      <slot />
    </div>
    <button @click="emitClose" class="modal-close is-large" aria-label="close"></button>
  </div>
</template>
<script>
export default {
  name: 'Modal',
  props: {
    active: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    emitClose () {
      this.$emit('close')
    }
  }
}
</script>
<style lang="scss" scoped>
.delete::before,
.modal-close::before,
.delete::after,
.modal-close::after {
  background-color: #fff;
}

.modal-close {
  background: $primary;

  &:hover {
    background: $primary;
  }
}
</style>
