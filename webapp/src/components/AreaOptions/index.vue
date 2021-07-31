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
    <span class="tag-area">
      <span class="material-icons-round mr-2">person_pin</span> 
      {{ totalUsers }} users in area
    </span>
  </div>
</template>
<script>
import { mapState } from 'vuex'

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
    emitChange (event) {
      this.$emit('change', event.target.value)
    }
  }
}
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

.tag-area {
  font-family: $family-dm-sans;
  font-size: 13px;
  font-weight: bold;
  display: flex;
  align-items: center;
  color: white;
  background: $primary;
  border-radius: 20px;
  height: 30px;
  padding: 20px;
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
