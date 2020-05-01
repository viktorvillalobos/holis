<template>
  <div class="connect-office-view">
    <hexagonal-grid :size="38" />
  </div>
</template>
<script>
import HexagonalGrid from "@/components/HexagonalGrid";

export default {
  name: "Office",
  components: {
    HexagonalGrid
  }
};
</script>
<style lang="scss">
.connect-office-view {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1;
}
</style>
