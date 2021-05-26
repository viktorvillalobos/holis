<template>
  <div class="connect-board-post-cta">
    <img :src="CTABg"/>
    <div class="columns content-footer">
      <p class="column is-four-fifths">¿Tienes algo muy bueno que contarle a todos?</p>
      <Btn @btn-click="emitAction" inverse class="column">¡Anúncialo!</Btn>
    </div>
  </div>
</template>
<script>
import Btn from '@/components/Btn'
import CTABg from '@/assets/boardWaves.svg'
export default {
  components: {
    Btn
  },
  data () {
    return {
      CTABg
    }
  },
  methods: {
    emitAction () {
      this.$emit('action')
    }
  }
}
</script>
<style lang="scss" scoped>
.connect-board-post-cta {
  p {
    color: white;
    margin: 0 10px 0 0;
  }
}

.connect-board-post-cta img{
  position: absolute;
  right: 0px;
  bottom: -1px;
  z-index: -1;
  width: 100%;
  height: auto;
}

.content-footer{
  bottom: 0px;
  padding-top: 20px;
  margin-left: 20px;
  margin-right: 40px;
}
</style>
