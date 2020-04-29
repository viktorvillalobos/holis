<template>
  <div class="connect-board-post-cta">
    <p>¿Tienes algo muy bueno que contarle a todos?</p>
    <Btn @btn-click="emitAction" inverse>¡Anúncialo!</Btn>
  </div>
</template>
<script>
import Btn from "@/components/Btn";
export default {
  components: {
    Btn
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
  padding: 0 5px 15px 5px;
  display: inline-flex;
  align-items: flex-end;
  justify-content: space-between;
  background: url(../../assets/boardWaves.svg);
  background-repeat: no-repeat;
  background-position: bottom;
  height: 65px;
  color: #fff;

  p {
    margin: 0 10px 0 0;
  }
}
</style>