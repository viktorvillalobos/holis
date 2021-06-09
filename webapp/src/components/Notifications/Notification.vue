<template>
  <div class="card m-2 hover-card" >
        <div class="card-content">
            <div class="media">
                <div class="media-left mt-4">
                    <img class="connect-logo-company" src="/static/images/logo/logo.svg" alt="espazum logo" width="60"/>
                </div>
                <div class="media-content">
                    <p class="is-size-6"><b>Chat</b></p>
                    <p class="is-size-7"><b>Luis Tundisi </b> te envio un mensaje</p>
                </div>

                <div class="media-right" align="right">
                    <p class="is-size-7" style="color:#A9A9A9">19, Julio, 2020</p>
                </div>
            </div>
        </div>
  </div>
</template>
<script>
import Card from '@/components/Card'
import Btn from '@/components/Btn'
export default {
  name: 'NotificationCard',
  props: {
    active: {
      type: Boolean,
      default: false
    },
    img: {
      type: String
    },
    asideOpened: {
      type: Boolean
    }
  },
  components: {
    Card,
    Btn
  },
  methods: {
    handleClose () {
      this.$emit('close')
    }
  }
}
</script>
<style lang="scss">
.alert-days{
    padding: 2px;
    margin-left: 5px;
}

.hover-card{
   box-shadow: 0px 0px 0px grey;
   transition: box-shadow .6s ease-out;
  -webkit-transition:  box-shadow .6s ease-out;
  box-shadow: .8px .9px 3px grey; 
}
.hover-card:hover{ 
     box-shadow: 1px 8px 10px grey;
     transition: box-shadow .6s ease-in;
    -webkit-transition:  box-shadow .6s ease-in;
}
</style>
