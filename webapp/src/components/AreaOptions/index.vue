<template>
  <div :class="['connect-area-options', {'aside-opened' : asideOpened}]">
    <div class="control">
      <div class="select is-small">
        <select>
          <option v-for="item in items" :key="item.id" :selected="item.name === current.name">{{item.name}}</option>
        </select>
      </div>
    </div>
    <span class="tag is-primary">12 usuarios conectados</span>
  </div>
</template>
<script>
export default {
  name: 'AreaOptions',
  props: {
    asideOpened: {
      type: Boolean
    },
    items: {
      type: Array
    },
    current: {
      type: Object
    }
  }
};
</script>
<style lang="scss" scoped>
.connect-area-options {
  position: fixed;
  bottom: 11px;
  display: flex;
  align-items: center;
  left: $margin-left-container;
  transition: $aside-transition;

  &.aside-opened {
    left: $margin-left-container-aside-opened;
  }
}

.tag {
  margin-left: 10px;
}

.select:not(.is-multiple):not(.is-loading)::after {
  z-index: 15;
  border-color: $font-color;
}

.select select {
  background: $light-gray;
  border-color: transparent;
}
</style>