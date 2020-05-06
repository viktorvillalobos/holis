<template>
  <div class="connect-area-options">
    <div class="control">
      <div class="select is-small">
        <select>
          <option selected>Slytherin</option>
          <option>Ravenclaw</option>
          <option>Hufflepuff</option>
          <option>Gryffindor</option>
        </select>
      </div>
    </div>
    <span class="tag is-primary">12 usuarios conectados</span>
  </div>
</template>
<script>
export default {};
</script>
<style lang="scss" scoped>
.connect-area-options {
    position: fixed;
    bottom: 11px;
    left: 9px;
    display: flex;
    align-items: center;
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