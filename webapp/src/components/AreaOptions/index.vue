<template>
  <div :class="['connect-area-options', {'aside-opened' : asideOpened}]">
    <div class="control" v-if="items.length > 1">
      <div class="select is-small">
        <select @change="emitChange">
          <option
            v-for="item in items"
            :key="item.id"
            :selected="item.name === current.name"
          >{{item.name}}</option>
        </select>
      </div>
    </div>
    <span class="tag is-primary">{{ totalUsers }} usuarios conectados</span>
  </div>
</template>
<script>
import { mapState } from 'vuex'

export default {
  name: "AreaOptions",
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
  },
  computed: {
    ...mapState({
      currentArea: state => state.areas.currentArea
    }),
    totalUsers () {
      if (!this.currentArea || !this.currentArea.state) {
        return 0
      }
      return this.currentArea.state.length
    }
  },
  methods: {
    emitChange(event) {
      this.$emit("change", event.target.value);
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
