<template>
  <div class="connect-board-post-cta" :style="`background-image: url(${CTABg})`">
    <p>¿Tienes algo muy bueno que contarle a todos?</p>
    <Btn @btn-click="emitAction" inverse>¡Anúncialo!</Btn>
  </div>
</template>
<script>
import Btn from "@/components/Btn";
import CTABg from "@/assets/boardWaves.svg"
export default {
  components: {
    Btn
  },
  data() {
    return {
      CTABg
    }
  },
  methods: {
    emitAction() {
      this.$emit('action')
    }
  }
};
</script>
<style lang="scss" scoped>
.connect-board-post-cta {
  position: absolute;
  bottom: 0;
  left: 0;
  padding: 0 5px 5px 5px;
  display: inline-flex;
  align-items: flex-end;
  justify-content: space-between;
  background-repeat: no-repeat;
  background-position: bottom;
  height: 90px;
  color: #fff;

  p {
    margin: 0 10px 0 0;
  }
}
</style>