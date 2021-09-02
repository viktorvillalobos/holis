<template>
  <div>
    <CreateGroup v-if="screen == 'index'" @send="updateScreen"/>
    <CreateGroupParticipants v-else @send="updateScreen" v-bind:dataGroup="this.dataGroup"  />
  </div>
</template>

<script>

import CreateGroup from "./CreateGroup"
import CreateGroupParticipants from "./CreateGroupParticipants"

export default {
  name: 'ChatGroup',
  components:{
    CreateGroup,
    CreateGroupParticipants
  },
  data () {
    return {
      screen: 'index',
      dataGroup: {}
    }
  },
  methods:{
    updateScreen(screen, data) {
      console.log(data)
      this.dataGroup = data
        this.screen = screen
    }
  }
}
</script>

<style lang="scss">
</style>
