<template>
  <div class="inbox">
    <div class="columns">
        <div class="column columns">
            <Avatar class="column" :img="recent.avatar_thumb" :text="recent.name" />
            <div class="column">
                <b>{{recent ? recent.name : 'Nombre misterioso' }}</b>
                <p>Texto de ejemplo de ultimo mensaje</p>
            </div>
        </div>
        <div class="column" style="justify-content: flex-end;">
            <div>
                <b>15:52</b>
            </div>
            <div>
                <font-awesome-icon icon="chevron-right" size="3x"/>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import Avatar from '@/components/Avatar'

export default {
  name: 'InboxMessage',
  components: {
      Avatar
  },
  props:["recent"],
  data () {
    return {}
  },
  created(){
      console.log("sexo anal")
  }
}
</script>

<style lang="scss">
.inbox{
    padding: 10px;
}
</style>
